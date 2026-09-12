from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.domain import (
    ActorType,
    AuditEvent,
    DecisionType,
    Evidence,
    PackageStatus,
    ResearchDecision,
    ResearchMode,
    ResearchProject,
    ResearchScope,
    ResearchStage,
    ResearchWorkflow,
    StagePackage,
    WorkflowState,
)

MACHINE_TRANSITIONS = {
    WorkflowState.DRAFT: {WorkflowState.SCOPED},
    WorkflowState.SCOPED: {WorkflowState.COLLECTING},
    WorkflowState.COLLECTING: {WorkflowState.DATA_VALIDATION},
    WorkflowState.DATA_VALIDATION: {WorkflowState.DATA_REVIEW, WorkflowState.BLOCKED},
    WorkflowState.DATA_APPROVED: {WorkflowState.ANALYZING},
    WorkflowState.ANALYZING: {WorkflowState.ANALYSIS_REVIEW, WorkflowState.BLOCKED},
    WorkflowState.STAGE_APPROVED: {WorkflowState.NEXT_STAGE},
    WorkflowState.NEXT_STAGE: {WorkflowState.COLLECTING, WorkflowState.COMPLETED},
}

STAGE_SEQUENCE = {
    ResearchMode.DISCOVERY: [
        ResearchStage.SCOPE,
        ResearchStage.MARKET,
        ResearchStage.CATEGORY,
        ResearchStage.NICHE,
        ResearchStage.CUSTOMER,
        ResearchStage.SEARCH_DEMAND,
        ResearchStage.PRODUCT,
        ResearchStage.CONTENT,
        ResearchStage.CONTENT_GAP,
        ResearchStage.AFF_ECONOMICS,
        ResearchStage.STRATEGY,
    ],
    ResearchMode.DEEP_RESEARCH: [
        ResearchStage.SCOPE,
        ResearchStage.CATEGORY,
        ResearchStage.NICHE,
        ResearchStage.CUSTOMER,
        ResearchStage.SEARCH_DEMAND,
        ResearchStage.PRODUCT,
        ResearchStage.CONTENT,
        ResearchStage.CONTENT_GAP,
        ResearchStage.AFF_ECONOMICS,
        ResearchStage.STRATEGY,
    ],
    ResearchMode.CUSTOMER_FIRST: [
        ResearchStage.SCOPE,
        ResearchStage.CUSTOMER,
        ResearchStage.SEARCH_DEMAND,
        ResearchStage.CATEGORY,
        ResearchStage.NICHE,
        ResearchStage.PRODUCT,
        ResearchStage.CONTENT,
        ResearchStage.CONTENT_GAP,
        ResearchStage.AFF_ECONOMICS,
        ResearchStage.STRATEGY,
    ],
    ResearchMode.KEYWORD_FIRST: [
        ResearchStage.SCOPE,
        ResearchStage.SEARCH_DEMAND,
        ResearchStage.CUSTOMER,
        ResearchStage.CATEGORY,
        ResearchStage.NICHE,
        ResearchStage.PRODUCT,
        ResearchStage.CONTENT,
        ResearchStage.CONTENT_GAP,
        ResearchStage.AFF_ECONOMICS,
        ResearchStage.STRATEGY,
    ],
}


def audit(
    db: Session,
    workflow: ResearchWorkflow,
    actor_type: ActorType,
    actor_id: str,
    action: str,
    old_state: WorkflowState | None,
    new_state: WorkflowState | None,
    reason: str | None = None,
    refs: list[str] | None = None,
) -> None:
    db.add(
        AuditEvent(
            project_id=workflow.project_id,
            stage=workflow.current_stage,
            actor_type=actor_type,
            actor_id=actor_id,
            action=action,
            old_state=old_state,
            new_state=new_state,
            reason=reason,
            object_refs=refs or [],
        )
    )


def machine_transition(
    db: Session,
    workflow: ResearchWorkflow,
    target: WorkflowState,
    actor_id: str = "system",
    reason: str | None = None,
) -> ResearchWorkflow:
    if target not in MACHINE_TRANSITIONS.get(workflow.state, set()):
        raise HTTPException(
            409, f"invalid machine transition: {workflow.state.value} -> {target.value}"
        )
    old = workflow.state
    if old == WorkflowState.NEXT_STAGE:
        project = db.get(ResearchProject, workflow.project_id)
        sequence = STAGE_SEQUENCE[project.mode]
        index = sequence.index(workflow.current_stage)
        if target == WorkflowState.COMPLETED:
            if index != len(sequence) - 1:
                raise HTTPException(409, "project cannot complete before the final stage")
            project.status = "COMPLETED"
        else:
            if index == len(sequence) - 1:
                raise HTTPException(409, "final stage must transition to COMPLETED")
            workflow.current_stage = sequence[index + 1]
    workflow.state = target
    audit(db, workflow, ActorType.MACHINE, actor_id, "MACHINE_TRANSITION", old, target, reason)
    db.commit()
    db.refresh(workflow)
    return workflow


def validate_package_evidence(db: Session, project_id: str, evidence_ids: list[str]) -> None:
    if not evidence_ids:
        return
    records = db.scalars(select(Evidence).where(Evidence.id.in_(evidence_ids))).all()
    if len(records) != len(set(evidence_ids)) or any(e.project_id != project_id for e in records):
        raise HTTPException(422, "all evidence must exist in this project")
    if any(e.rejected for e in records):
        raise HTTPException(422, "rejected evidence cannot enter a stage package")


def create_package(db: Session, workflow: ResearchWorkflow, data) -> StagePackage:
    validate_package_evidence(db, workflow.project_id, data.evidence_ids)
    version = (
        db.scalar(
            select(func.max(StagePackage.version)).where(
                StagePackage.project_id == workflow.project_id,
                StagePackage.stage == workflow.current_stage,
            )
        )
        or 0
    ) + 1
    package = StagePackage(
        project_id=workflow.project_id,
        stage=workflow.current_stage,
        version=version,
        **data.model_dump(),
    )
    db.add(package)
    db.flush()
    audit(
        db,
        workflow,
        ActorType.HUMAN,
        "package-author",
        "PACKAGE_CREATED",
        workflow.state,
        workflow.state,
        refs=[package.id],
    )
    db.commit()
    db.refresh(package)
    return package


def human_decision(db: Session, workflow: ResearchWorkflow, data) -> ResearchWorkflow:
    if data.actor_type != ActorType.HUMAN:
        raise HTTPException(403, "human approval gates require a HUMAN actor")
    old = workflow.state
    new = old
    if data.decision == DecisionType.APPROVE:
        if old == WorkflowState.DATA_REVIEW:
            new = WorkflowState.DATA_APPROVED
        elif old == WorkflowState.ANALYSIS_REVIEW:
            package = db.scalar(
                select(StagePackage)
                .where(
                    StagePackage.project_id == workflow.project_id,
                    StagePackage.stage == workflow.current_stage,
                    StagePackage.status == PackageStatus.DRAFT,
                )
                .order_by(StagePackage.version.desc())
            )
            if package is None:
                raise HTTPException(
                    409, "a draft stage package is required before analysis approval"
                )
            validate_package_evidence(db, workflow.project_id, package.evidence_ids)
            package.status = PackageStatus.APPROVED
            package.approved_by = data.actor_id
            package.approved_at = datetime.now(UTC)
            new = WorkflowState.STAGE_APPROVED
            data.object_refs.append(package.id)
        else:
            raise HTTPException(409, f"APPROVE is not valid from {old.value}")
    elif data.decision == DecisionType.REJECT:
        if old not in {WorkflowState.DATA_REVIEW, WorkflowState.ANALYSIS_REVIEW}:
            raise HTTPException(409, "REJECT requires a review state")
        new = WorkflowState.BLOCKED
        workflow.blocked_reason = data.reason or "Rejected by human reviewer"
    elif data.decision == DecisionType.RESEARCH_MORE:
        if old not in {WorkflowState.DATA_REVIEW, WorkflowState.ANALYSIS_REVIEW}:
            raise HTTPException(409, "RESEARCH_MORE requires a review state")
        latest = db.scalar(
            select(ResearchScope)
            .where(ResearchScope.project_id == workflow.project_id)
            .order_by(ResearchScope.version.desc())
        )
        if latest is None:
            raise HTTPException(409, "an existing scope is required")
        copy = ResearchScope(
            project_id=latest.project_id,
            parent_scope_id=latest.id,
            version=latest.version + 1,
            category_ids=latest.category_ids,
            seed_keywords=latest.seed_keywords,
            customer_hypotheses=latest.customer_hypotheses,
            platforms=latest.platforms,
            date_from=latest.date_from,
            date_to=latest.date_to,
            geography=latest.geography,
            max_results=latest.max_results,
            created_by=data.actor_id,
        )
        db.add(copy)
        new = WorkflowState.COLLECTING
        data.object_refs.append(copy.id)
    elif data.decision == DecisionType.GO_BACK:
        project = db.get(ResearchProject, workflow.project_id)
        sequence = STAGE_SEQUENCE[project.mode]
        index = sequence.index(workflow.current_stage)
        if index == 0:
            raise HTTPException(409, "already at first stage")
        workflow.current_stage = sequence[index - 1]
        new = WorkflowState.ANALYSIS_REVIEW
    elif data.decision == DecisionType.EDIT:
        if old not in {WorkflowState.DATA_REVIEW, WorkflowState.ANALYSIS_REVIEW}:
            raise HTTPException(409, "EDIT requires a review state")
    workflow.state = new
    decision = ResearchDecision(
        project_id=workflow.project_id,
        stage=workflow.current_stage,
        decision=data.decision,
        actor_type=data.actor_type,
        actor_id=data.actor_id,
        reason=data.reason,
        old_state=old,
        new_state=new,
        object_refs=data.object_refs,
    )
    db.add(decision)
    audit(
        db,
        workflow,
        data.actor_type,
        data.actor_id,
        data.decision.value,
        old,
        new,
        data.reason,
        data.object_refs,
    )
    db.commit()
    db.refresh(workflow)
    return workflow
