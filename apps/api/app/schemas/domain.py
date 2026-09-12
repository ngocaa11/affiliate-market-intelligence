from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.domain import (
    ActorType,
    DecisionType,
    EvidenceActionType,
    EvidenceType,
    FreshnessStatus,
    PackageStatus,
    ProjectStatus,
    ResearchMode,
    ResearchStage,
    WorkflowState,
)


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    mode: ResearchMode
    objective: str = Field(min_length=1)
    market: str = "Vietnam"
    locale: str = "vi-VN"
    time_horizon_days: int = Field(default=90, ge=1, le=3650)
    created_by: str = Field(min_length=1, max_length=100)


class ProjectRead(ORMModel):
    id: str
    name: str
    mode: ResearchMode
    objective: str
    market: str
    locale: str
    time_horizon_days: int
    status: ProjectStatus
    created_by: str
    created_at: datetime
    updated_at: datetime


class ScopeCreate(BaseModel):
    category_ids: list[str] = []
    seed_keywords: list[str] = []
    customer_hypotheses: list[str] = []
    platforms: list[str] = ["SHOPEE"]
    date_from: str | None = None
    date_to: str | None = None
    geography: str = "Vietnam"
    max_results: int = Field(default=100, ge=1, le=10000)
    created_by: str = Field(min_length=1)
    parent_scope_id: str | None = None


class ScopeRead(ORMModel):
    id: str
    project_id: str
    parent_scope_id: str | None
    version: int
    category_ids: list[str]
    seed_keywords: list[str]
    customer_hypotheses: list[str]
    platforms: list[str]
    date_from: str | None
    date_to: str | None
    geography: str
    max_results: int
    created_by: str
    created_at: datetime


class WorkflowRead(ORMModel):
    id: str
    project_id: str
    current_stage: ResearchStage
    state: WorkflowState
    blocked_reason: str | None
    updated_at: datetime


class MachineTransition(BaseModel):
    target_state: WorkflowState
    actor_id: str = "system"
    reason: str | None = None


class PackageCreate(BaseModel):
    selected_entities: list[Any] = []
    metrics: dict[str, Any] = {}
    evidence_ids: list[str] = []
    user_note_ids: list[str] = []
    claims: list[Any] = []
    confidence: float | None = Field(default=None, ge=0, le=1)
    coverage: float | None = Field(default=None, ge=0, le=1)
    freshness: dict[str, Any] = {}
    parent_package_id: str | None = None


class PackageRead(ORMModel):
    id: str
    project_id: str
    stage: ResearchStage
    version: int
    parent_package_id: str | None
    status: PackageStatus
    selected_entities: list[Any]
    metrics: dict[str, Any]
    evidence_ids: list[str]
    user_note_ids: list[str]
    claims: list[Any]
    confidence: float | None
    coverage: float | None
    freshness: dict[str, Any]
    approved_by: str | None
    approved_at: datetime | None
    created_at: datetime


class EvidenceCreate(BaseModel):
    evidence_type: EvidenceType
    entity_ref: str | None = None
    summary: str = Field(min_length=1)
    source_ref: str = Field(min_length=1)
    captured_at: datetime
    confidence: float = Field(ge=0, le=1)
    freshness: FreshnessStatus = FreshnessStatus.UNKNOWN
    estimated: bool = False
    estimation_method: str | None = None

    @model_validator(mode="after")
    def require_estimation_method(self):
        if self.estimated and not self.estimation_method:
            raise ValueError("estimated evidence requires estimation_method")
        return self


class EvidenceRead(ORMModel):
    id: str
    project_id: str
    evidence_type: EvidenceType
    entity_ref: str | None
    summary: str
    source_ref: str
    captured_at: datetime
    confidence: float
    freshness: FreshnessStatus
    estimated: bool
    estimation_method: str | None
    pinned: bool
    rejected: bool
    created_at: datetime


class EvidenceActionCreate(BaseModel):
    action: EvidenceActionType
    actor_id: str = Field(min_length=1)
    reason: str | None = None


class NoteCreate(BaseModel):
    stage: ResearchStage
    evidence_id: str | None = None
    text: str = Field(min_length=1)
    created_by: str = Field(min_length=1)


class NoteRead(ORMModel):
    id: str
    project_id: str
    stage: ResearchStage
    evidence_id: str | None
    text: str
    created_by: str
    created_at: datetime


class DecisionCreate(BaseModel):
    decision: DecisionType
    actor_type: ActorType
    actor_id: str = Field(min_length=1)
    reason: str | None = None
    object_refs: list[str] = []


class AuditRead(ORMModel):
    id: str
    project_id: str
    stage: ResearchStage
    actor_type: ActorType
    actor_id: str
    action: str
    old_state: WorkflowState | None
    new_state: WorkflowState | None
    reason: str | None
    object_refs: list[str]
    created_at: datetime
