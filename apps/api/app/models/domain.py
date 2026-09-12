import uuid
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def uuid4_str() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    return datetime.now(UTC)


class ResearchMode(StrEnum):
    DISCOVERY = "DISCOVERY"
    DEEP_RESEARCH = "DEEP_RESEARCH"
    CUSTOMER_FIRST = "CUSTOMER_FIRST"
    KEYWORD_FIRST = "KEYWORD_FIRST"


class ProjectStatus(StrEnum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    BLOCKED = "BLOCKED"


class ResearchStage(StrEnum):
    SCOPE = "SCOPE"
    MARKET = "MARKET"
    CATEGORY = "CATEGORY"
    NICHE = "NICHE"
    CUSTOMER = "CUSTOMER"
    SEARCH_DEMAND = "SEARCH_DEMAND"
    PRODUCT = "PRODUCT"
    CONTENT = "CONTENT"
    CONTENT_GAP = "CONTENT_GAP"
    AFF_ECONOMICS = "AFF_ECONOMICS"
    STRATEGY = "STRATEGY"


class WorkflowState(StrEnum):
    DRAFT = "DRAFT"
    SCOPED = "SCOPED"
    COLLECTING = "COLLECTING"
    DATA_VALIDATION = "DATA_VALIDATION"
    DATA_REVIEW = "DATA_REVIEW"
    DATA_APPROVED = "DATA_APPROVED"
    ANALYZING = "ANALYZING"
    ANALYSIS_REVIEW = "ANALYSIS_REVIEW"
    STAGE_APPROVED = "STAGE_APPROVED"
    NEXT_STAGE = "NEXT_STAGE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    BLOCKED = "BLOCKED"


class ActorType(StrEnum):
    HUMAN = "HUMAN"
    MACHINE = "MACHINE"
    AI = "AI"


class DecisionType(StrEnum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    EDIT = "EDIT"
    RESEARCH_MORE = "RESEARCH_MORE"
    GO_BACK = "GO_BACK"


class PackageStatus(StrEnum):
    DRAFT = "DRAFT"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"


class EvidenceType(StrEnum):
    METRIC = "METRIC"
    PRODUCT = "PRODUCT"
    KEYWORD = "KEYWORD"
    CONTENT = "CONTENT"
    USER_NOTE = "USER_NOTE"
    SOURCE_RECORD = "SOURCE_RECORD"
    CHART = "CHART"
    EXTERNAL_PROVIDER = "EXTERNAL_PROVIDER"


class EvidenceActionType(StrEnum):
    PIN = "PIN"
    REJECT = "REJECT"
    RESTORE = "RESTORE"


class FreshnessStatus(StrEnum):
    FRESH = "FRESH"
    STALE = "STALE"
    UNKNOWN = "UNKNOWN"


class ResearchProject(Base):
    __tablename__ = "research_projects"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid4_str)
    name: Mapped[str] = mapped_column(String(200))
    mode: Mapped[ResearchMode] = mapped_column(Enum(ResearchMode, native_enum=False))
    objective: Mapped[str] = mapped_column(Text)
    market: Mapped[str] = mapped_column(String(100), default="Vietnam")
    locale: Mapped[str] = mapped_column(String(20), default="vi-VN")
    time_horizon_days: Mapped[int] = mapped_column(Integer, default=90)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, native_enum=False), default=ProjectStatus.ACTIVE
    )
    created_by: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )
    workflow: Mapped["ResearchWorkflow"] = relationship(
        back_populates="project", uselist=False, cascade="all, delete-orphan"
    )


class ResearchScope(Base):
    __tablename__ = "research_scopes"
    __table_args__ = (UniqueConstraint("project_id", "version", name="uq_scope_project_version"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid4_str)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("research_projects.id", ondelete="CASCADE"), index=True
    )
    parent_scope_id: Mapped[str | None] = mapped_column(
        ForeignKey("research_scopes.id"), nullable=True
    )
    version: Mapped[int] = mapped_column(Integer)
    category_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    seed_keywords: Mapped[list[str]] = mapped_column(JSON, default=list)
    customer_hypotheses: Mapped[list[str]] = mapped_column(JSON, default=list)
    platforms: Mapped[list[str]] = mapped_column(JSON, default=list)
    date_from: Mapped[str | None] = mapped_column(String(10), nullable=True)
    date_to: Mapped[str | None] = mapped_column(String(10), nullable=True)
    geography: Mapped[str] = mapped_column(String(100), default="Vietnam")
    max_results: Mapped[int] = mapped_column(Integer, default=100)
    created_by: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class ResearchWorkflow(Base):
    __tablename__ = "research_workflows"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid4_str)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("research_projects.id", ondelete="CASCADE"), unique=True
    )
    current_stage: Mapped[ResearchStage] = mapped_column(
        Enum(ResearchStage, native_enum=False), default=ResearchStage.SCOPE
    )
    state: Mapped[WorkflowState] = mapped_column(
        Enum(WorkflowState, native_enum=False), default=WorkflowState.DRAFT
    )
    blocked_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )
    project: Mapped[ResearchProject] = relationship(back_populates="workflow")


class StagePackage(Base):
    __tablename__ = "stage_packages"
    __table_args__ = (
        UniqueConstraint("project_id", "stage", "version", name="uq_package_version"),
    )
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid4_str)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("research_projects.id", ondelete="CASCADE"), index=True
    )
    stage: Mapped[ResearchStage] = mapped_column(Enum(ResearchStage, native_enum=False))
    version: Mapped[int] = mapped_column(Integer)
    parent_package_id: Mapped[str | None] = mapped_column(
        ForeignKey("stage_packages.id"), nullable=True
    )
    status: Mapped[PackageStatus] = mapped_column(
        Enum(PackageStatus, native_enum=False), default=PackageStatus.DRAFT
    )
    selected_entities: Mapped[list[Any]] = mapped_column(JSON, default=list)
    metrics: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    evidence_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    user_note_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    claims: Mapped[list[Any]] = mapped_column(JSON, default=list)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    coverage: Mapped[float | None] = mapped_column(Float, nullable=True)
    freshness: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    approved_by: Mapped[str | None] = mapped_column(String(100), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Evidence(Base):
    __tablename__ = "evidence"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid4_str)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("research_projects.id", ondelete="CASCADE"), index=True
    )
    evidence_type: Mapped[EvidenceType] = mapped_column(Enum(EvidenceType, native_enum=False))
    entity_ref: Mapped[str | None] = mapped_column(String(200), nullable=True)
    summary: Mapped[str] = mapped_column(Text)
    source_ref: Mapped[str] = mapped_column(String(500))
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    confidence: Mapped[float] = mapped_column(Float)
    freshness: Mapped[FreshnessStatus] = mapped_column(Enum(FreshnessStatus, native_enum=False))
    estimated: Mapped[bool] = mapped_column(Boolean, default=False)
    estimation_method: Mapped[str | None] = mapped_column(Text, nullable=True)
    pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    rejected: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class EvidenceAction(Base):
    __tablename__ = "evidence_actions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid4_str)
    evidence_id: Mapped[str] = mapped_column(
        ForeignKey("evidence.id", ondelete="CASCADE"), index=True
    )
    action: Mapped[EvidenceActionType] = mapped_column(Enum(EvidenceActionType, native_enum=False))
    actor_id: Mapped[str] = mapped_column(String(100))
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class UserNote(Base):
    __tablename__ = "user_notes"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid4_str)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("research_projects.id", ondelete="CASCADE"), index=True
    )
    stage: Mapped[ResearchStage] = mapped_column(Enum(ResearchStage, native_enum=False))
    evidence_id: Mapped[str | None] = mapped_column(ForeignKey("evidence.id"), nullable=True)
    text: Mapped[str] = mapped_column(Text)
    created_by: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class ResearchDecision(Base):
    __tablename__ = "research_decisions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid4_str)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("research_projects.id", ondelete="CASCADE"), index=True
    )
    stage: Mapped[ResearchStage] = mapped_column(Enum(ResearchStage, native_enum=False))
    decision: Mapped[DecisionType] = mapped_column(Enum(DecisionType, native_enum=False))
    actor_type: Mapped[ActorType] = mapped_column(Enum(ActorType, native_enum=False))
    actor_id: Mapped[str] = mapped_column(String(100))
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    old_state: Mapped[WorkflowState] = mapped_column(Enum(WorkflowState, native_enum=False))
    new_state: Mapped[WorkflowState] = mapped_column(Enum(WorkflowState, native_enum=False))
    object_refs: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid4_str)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("research_projects.id", ondelete="CASCADE"), index=True
    )
    stage: Mapped[ResearchStage] = mapped_column(Enum(ResearchStage, native_enum=False))
    actor_type: Mapped[ActorType] = mapped_column(Enum(ActorType, native_enum=False))
    actor_id: Mapped[str] = mapped_column(String(100))
    action: Mapped[str] = mapped_column(String(100))
    old_state: Mapped[WorkflowState | None] = mapped_column(
        Enum(WorkflowState, native_enum=False), nullable=True
    )
    new_state: Mapped[WorkflowState | None] = mapped_column(
        Enum(WorkflowState, native_enum=False), nullable=True
    )
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    object_refs: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
