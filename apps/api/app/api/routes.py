from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.models.domain import (
    ActorType,
    AuditEvent,
    Evidence,
    EvidenceAction,
    EvidenceActionType,
    ResearchProject,
    ResearchScope,
    ResearchWorkflow,
    StagePackage,
    UserNote,
    WorkflowState,
)
from app.schemas.domain import (
    AuditRead,
    DecisionCreate,
    EvidenceActionCreate,
    EvidenceCreate,
    EvidenceRead,
    MachineTransition,
    NoteCreate,
    NoteRead,
    PackageCreate,
    PackageRead,
    ProjectCreate,
    ProjectRead,
    ScopeCreate,
    ScopeRead,
    WorkflowRead,
)
from app.services.workflow import audit, create_package, human_decision, machine_transition

router = APIRouter()


def project_or_404(db: Session, project_id: str) -> ResearchProject:
    project = db.get(ResearchProject, project_id)
    if project is None:
        raise HTTPException(404, "project not found")
    return project


def workflow_or_404(db: Session, project_id: str) -> ResearchWorkflow:
    workflow = db.scalar(select(ResearchWorkflow).where(ResearchWorkflow.project_id == project_id))
    if workflow is None:
        raise HTTPException(404, "workflow not found")
    return workflow


@router.get("/health")
def health():
    settings = get_settings()
    return {"status": "ok", "service": settings.app_name, "environment": settings.app_env}


@router.post("/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    project = ResearchProject(**data.model_dump())
    workflow = ResearchWorkflow(project=project)
    db.add_all([project, workflow])
    db.flush()
    audit(
        db,
        workflow,
        ActorType.HUMAN,
        data.created_by,
        "PROJECT_CREATED",
        None,
        WorkflowState.DRAFT,
        refs=[project.id],
    )
    db.commit()
    db.refresh(project)
    return project


@router.get("/projects", response_model=list[ProjectRead])
def list_projects(db: Session = Depends(get_db)):
    return db.scalars(select(ResearchProject).order_by(ResearchProject.created_at.desc())).all()


@router.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: str, db: Session = Depends(get_db)):
    return project_or_404(db, project_id)


@router.post("/projects/{project_id}/scopes", response_model=ScopeRead, status_code=201)
def create_scope(project_id: str, data: ScopeCreate, db: Session = Depends(get_db)):
    project_or_404(db, project_id)
    workflow = workflow_or_404(db, project_id)
    if workflow.state not in {
        WorkflowState.DRAFT,
        WorkflowState.DATA_REVIEW,
        WorkflowState.ANALYSIS_REVIEW,
        WorkflowState.BLOCKED,
    }:
        raise HTTPException(409, "scope cannot be changed in the current workflow state")
    version = (
        db.scalar(
            select(func.max(ResearchScope.version)).where(ResearchScope.project_id == project_id)
        )
        or 0
    ) + 1
    if data.parent_scope_id:
        parent = db.get(ResearchScope, data.parent_scope_id)
        if parent is None or parent.project_id != project_id:
            raise HTTPException(422, "parent scope must belong to this project")
    scope = ResearchScope(project_id=project_id, version=version, **data.model_dump())
    db.add(scope)
    db.flush()
    old = workflow.state
    if old == WorkflowState.DRAFT:
        workflow.state = WorkflowState.SCOPED
    audit(
        db,
        workflow,
        ActorType.HUMAN,
        data.created_by,
        "SCOPE_VERSION_CREATED",
        old,
        workflow.state,
        refs=[scope.id],
    )
    db.commit()
    db.refresh(scope)
    return scope


@router.get("/projects/{project_id}/scopes", response_model=list[ScopeRead])
def list_scopes(project_id: str, db: Session = Depends(get_db)):
    project_or_404(db, project_id)
    return db.scalars(
        select(ResearchScope)
        .where(ResearchScope.project_id == project_id)
        .order_by(ResearchScope.version.desc())
    ).all()


@router.get("/projects/{project_id}/workflow", response_model=WorkflowRead)
def get_workflow(project_id: str, db: Session = Depends(get_db)):
    project_or_404(db, project_id)
    return workflow_or_404(db, project_id)


@router.post("/projects/{project_id}/machine-transitions", response_model=WorkflowRead)
def transition(project_id: str, data: MachineTransition, db: Session = Depends(get_db)):
    project_or_404(db, project_id)
    return machine_transition(
        db, workflow_or_404(db, project_id), data.target_state, data.actor_id, data.reason
    )


@router.post("/projects/{project_id}/decisions", response_model=WorkflowRead)
def decide(project_id: str, data: DecisionCreate, db: Session = Depends(get_db)):
    project_or_404(db, project_id)
    return human_decision(db, workflow_or_404(db, project_id), data)


@router.post("/projects/{project_id}/packages", response_model=PackageRead, status_code=201)
def add_package(project_id: str, data: PackageCreate, db: Session = Depends(get_db)):
    project_or_404(db, project_id)
    return create_package(db, workflow_or_404(db, project_id), data)


@router.get("/projects/{project_id}/packages", response_model=list[PackageRead])
def list_packages(project_id: str, db: Session = Depends(get_db)):
    project_or_404(db, project_id)
    return db.scalars(
        select(StagePackage)
        .where(StagePackage.project_id == project_id)
        .order_by(StagePackage.created_at.desc())
    ).all()


@router.post("/projects/{project_id}/evidence", response_model=EvidenceRead, status_code=201)
def add_evidence(project_id: str, data: EvidenceCreate, db: Session = Depends(get_db)):
    project_or_404(db, project_id)
    workflow = workflow_or_404(db, project_id)
    evidence = Evidence(project_id=project_id, **data.model_dump())
    db.add(evidence)
    db.flush()
    audit(
        db,
        workflow,
        ActorType.MACHINE,
        "evidence-service",
        "EVIDENCE_CREATED",
        workflow.state,
        workflow.state,
        refs=[evidence.id],
    )
    db.commit()
    db.refresh(evidence)
    return evidence


@router.get("/projects/{project_id}/evidence", response_model=list[EvidenceRead])
def list_evidence(project_id: str, db: Session = Depends(get_db)):
    project_or_404(db, project_id)
    return db.scalars(
        select(Evidence)
        .where(Evidence.project_id == project_id)
        .order_by(Evidence.created_at.desc())
    ).all()


@router.post("/projects/{project_id}/evidence/{evidence_id}/actions", response_model=EvidenceRead)
def act_on_evidence(
    project_id: str, evidence_id: str, data: EvidenceActionCreate, db: Session = Depends(get_db)
):
    evidence = db.get(Evidence, evidence_id)
    if evidence is None or evidence.project_id != project_id:
        raise HTTPException(404, "evidence not found")
    if data.action == EvidenceActionType.PIN:
        evidence.pinned, evidence.rejected = True, False
    elif data.action == EvidenceActionType.REJECT:
        evidence.pinned, evidence.rejected = False, True
    else:
        evidence.pinned, evidence.rejected = False, False
    db.add(
        EvidenceAction(
            evidence_id=evidence.id, action=data.action, actor_id=data.actor_id, reason=data.reason
        )
    )
    workflow = workflow_or_404(db, project_id)
    audit(
        db,
        workflow,
        ActorType.HUMAN,
        data.actor_id,
        f"EVIDENCE_{data.action.value}",
        workflow.state,
        workflow.state,
        data.reason,
        [evidence.id],
    )
    db.commit()
    db.refresh(evidence)
    return evidence


@router.post("/projects/{project_id}/notes", response_model=NoteRead, status_code=201)
def add_note(project_id: str, data: NoteCreate, db: Session = Depends(get_db)):
    project_or_404(db, project_id)
    if data.evidence_id:
        evidence = db.get(Evidence, data.evidence_id)
        if evidence is None or evidence.project_id != project_id:
            raise HTTPException(422, "evidence must belong to this project")
    note = UserNote(project_id=project_id, **data.model_dump())
    db.add(note)
    db.flush()
    workflow = workflow_or_404(db, project_id)
    audit(
        db,
        workflow,
        ActorType.HUMAN,
        data.created_by,
        "NOTE_ADDED",
        workflow.state,
        workflow.state,
        refs=[note.id],
    )
    db.commit()
    db.refresh(note)
    return note


@router.get("/projects/{project_id}/notes", response_model=list[NoteRead])
def list_notes(project_id: str, db: Session = Depends(get_db)):
    project_or_404(db, project_id)
    return db.scalars(
        select(UserNote)
        .where(UserNote.project_id == project_id)
        .order_by(UserNote.created_at.desc())
    ).all()


@router.get("/projects/{project_id}/audit", response_model=list[AuditRead])
def list_audit(project_id: str, db: Session = Depends(get_db)):
    project_or_404(db, project_id)
    return db.scalars(
        select(AuditEvent)
        .where(AuditEvent.project_id == project_id)
        .order_by(AuditEvent.created_at.desc())
    ).all()
