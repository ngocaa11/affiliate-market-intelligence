"""Phase A foundation schema.

Revision ID: 0001
"""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "research_projects",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("mode", sa.String(30), nullable=False),
        sa.Column("objective", sa.Text(), nullable=False),
        sa.Column("market", sa.String(100), nullable=False),
        sa.Column("locale", sa.String(20), nullable=False),
        sa.Column("time_horizon_days", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("created_by", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "research_workflows",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "project_id",
            sa.String(36),
            sa.ForeignKey("research_projects.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("current_stage", sa.String(30), nullable=False),
        sa.Column("state", sa.String(30), nullable=False),
        sa.Column("blocked_reason", sa.Text()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "research_scopes",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "project_id",
            sa.String(36),
            sa.ForeignKey("research_projects.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("parent_scope_id", sa.String(36), sa.ForeignKey("research_scopes.id")),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("category_ids", sa.JSON(), nullable=False),
        sa.Column("seed_keywords", sa.JSON(), nullable=False),
        sa.Column("customer_hypotheses", sa.JSON(), nullable=False),
        sa.Column("platforms", sa.JSON(), nullable=False),
        sa.Column("date_from", sa.String(10)),
        sa.Column("date_to", sa.String(10)),
        sa.Column("geography", sa.String(100), nullable=False),
        sa.Column("max_results", sa.Integer(), nullable=False),
        sa.Column("created_by", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("project_id", "version", name="uq_scope_project_version"),
    )
    op.create_table(
        "stage_packages",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "project_id",
            sa.String(36),
            sa.ForeignKey("research_projects.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("stage", sa.String(30), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("parent_package_id", sa.String(36), sa.ForeignKey("stage_packages.id")),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("selected_entities", sa.JSON(), nullable=False),
        sa.Column("metrics", sa.JSON(), nullable=False),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        sa.Column("user_note_ids", sa.JSON(), nullable=False),
        sa.Column("claims", sa.JSON(), nullable=False),
        sa.Column("confidence", sa.Float()),
        sa.Column("coverage", sa.Float()),
        sa.Column("freshness", sa.JSON(), nullable=False),
        sa.Column("approved_by", sa.String(100)),
        sa.Column("approved_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("project_id", "stage", "version", name="uq_package_version"),
    )
    op.create_table(
        "evidence",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "project_id",
            sa.String(36),
            sa.ForeignKey("research_projects.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("evidence_type", sa.String(30), nullable=False),
        sa.Column("entity_ref", sa.String(200)),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("source_ref", sa.String(500), nullable=False),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("freshness", sa.String(20), nullable=False),
        sa.Column("estimated", sa.Boolean(), nullable=False),
        sa.Column("estimation_method", sa.Text()),
        sa.Column("pinned", sa.Boolean(), nullable=False),
        sa.Column("rejected", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "evidence_actions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "evidence_id",
            sa.String(36),
            sa.ForeignKey("evidence.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("action", sa.String(20), nullable=False),
        sa.Column("actor_id", sa.String(100), nullable=False),
        sa.Column("reason", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "user_notes",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "project_id",
            sa.String(36),
            sa.ForeignKey("research_projects.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("stage", sa.String(30), nullable=False),
        sa.Column("evidence_id", sa.String(36), sa.ForeignKey("evidence.id")),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("created_by", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "research_decisions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "project_id",
            sa.String(36),
            sa.ForeignKey("research_projects.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("stage", sa.String(30), nullable=False),
        sa.Column("decision", sa.String(30), nullable=False),
        sa.Column("actor_type", sa.String(20), nullable=False),
        sa.Column("actor_id", sa.String(100), nullable=False),
        sa.Column("reason", sa.Text()),
        sa.Column("old_state", sa.String(30), nullable=False),
        sa.Column("new_state", sa.String(30), nullable=False),
        sa.Column("object_refs", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "audit_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "project_id",
            sa.String(36),
            sa.ForeignKey("research_projects.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("stage", sa.String(30), nullable=False),
        sa.Column("actor_type", sa.String(20), nullable=False),
        sa.Column("actor_id", sa.String(100), nullable=False),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("old_state", sa.String(30)),
        sa.Column("new_state", sa.String(30)),
        sa.Column("reason", sa.Text()),
        sa.Column("object_refs", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    for table in (
        "audit_events",
        "research_decisions",
        "user_notes",
        "evidence_actions",
        "evidence",
        "stage_packages",
        "research_scopes",
        "research_workflows",
        "research_projects",
    ):
        op.drop_table(table)
