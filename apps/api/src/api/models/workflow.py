"""
NEXUS DESIGN AI - Workflow Models
"""

import enum
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    String, Text, DateTime, Enum, ForeignKey, JSON, Index, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from api.database import Base


class WorkflowStatus(str, enum.Enum):
    """Workflow execution status."""
    PENDING = "pending"
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowStepStatus(str, enum.Enum):
    """Individual workflow step status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class Workflow(Base):
    """Workflow execution record."""

    __tablename__ = "workflows"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[WorkflowStatus] = mapped_column(
        Enum(WorkflowStatus), default=WorkflowStatus.PENDING, nullable=False
    )

    # Workflow definition
    workflow_type: Mapped[str] = mapped_column(String(100), nullable=False)  # full_design, ui_only, etc.
    steps_definition: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=False)
    current_step: Mapped[int] = mapped_column(default=0)

    # Execution metadata
    total_tokens: Mapped[int] = mapped_column(default=0)
    total_cost: Mapped[Optional[float]] = mapped_column(nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="workflows", lazy="selectin")
    tasks: Mapped[List["AgentTask"]] = relationship("AgentTask", back_populates="workflow", lazy="selectin")
    steps: Mapped[List["WorkflowStep"]] = relationship("WorkflowStep", back_populates="workflow", lazy="selectin", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("ix_workflows_project_id", "project_id"),
        Index("ix_workflows_status", "status"),
    )

    def __repr__(self) -> str:
        return f"<Workflow(id={self.id}, name='{self.name}', status={self.status})>"


class WorkflowStep(Base):
    """Individual step within a workflow."""

    __tablename__ = "workflow_steps"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workflow_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False
    )
    step_number: Mapped[int] = mapped_column(nullable=False)
    agent_type: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[WorkflowStepStatus] = mapped_column(
        Enum(WorkflowStepStatus), default=WorkflowStepStatus.PENDING, nullable=False
    )

    # Step configuration
    input_schema: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    output_schema: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    config: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Execution results
    input_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    output_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tokens_used: Mapped[int] = mapped_column(default=0)
    execution_time: Mapped[Optional[float]] = mapped_column(nullable=True)

    # Human validation
    requires_approval: Mapped[bool] = mapped_column(default=False)
    approved: Mapped[Optional[bool]] = mapped_column(nullable=True)
    approval_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    workflow: Mapped["Workflow"] = relationship("Workflow", back_populates="steps", lazy="selectin")

    # Indexes
    __table_args__ = (
        Index("ix_workflow_steps_workflow_id", "workflow_id"),
        Index("ix_workflow_steps_step_number", "workflow_id", "step_number"),
    )

    def __repr__(self) -> str:
        return f"<WorkflowStep(id={self.id}, step={self.step_number}, agent={self.agent_type})>"