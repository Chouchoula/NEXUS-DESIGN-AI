"""
NEXUS DESIGN AI - Agent Task Models
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


class AgentType(str, enum.Enum):
    """Types of specialized agents."""
    ORCHESTRATOR = "orchestrator"
    RESEARCH = "research"
    ART_DIRECTOR = "art_director"
    UI_DESIGNER = "ui_designer"
    UX_DESIGNER = "ux_designer"
    FRONTEND_ENGINEER = "frontend_engineer"
    VISUAL_QA = "visual_qa"


class TaskStatus(str, enum.Enum):
    """Agent task status."""
    PENDING = "pending"
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentTask(Base):
    """Agent task execution record."""

    __tablename__ = "agent_tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    workflow_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="SET NULL"), nullable=True
    )
    agent_type: Mapped[AgentType] = mapped_column(Enum(AgentType), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False
    )

    # Task definition
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    input_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    output_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Execution metadata
    model_provider: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    model_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    tokens_used: Mapped[int] = mapped_column(default=0)
    execution_time: Mapped[Optional[float]] = mapped_column(nullable=True)  # seconds
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(default=0)

    # Human validation
    requires_approval: Mapped[bool] = mapped_column(default=False)
    approved_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

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
    project: Mapped["Project"] = relationship("Project", back_populates="tasks", lazy="selectin")
    workflow: Mapped[Optional["Workflow"]] = relationship("Workflow", back_populates="tasks", lazy="selectin")

    # Indexes
    __table_args__ = (
        Index("ix_agent_tasks_project_id", "project_id"),
        Index("ix_agent_tasks_agent_type", "agent_type"),
        Index("ix_agent_tasks_status", "status"),
        Index("ix_agent_tasks_workflow_id", "workflow_id"),
    )

    def __repr__(self) -> str:
        return f"<AgentTask(id={self.id}, agent={self.agent_type}, status={self.status})>"