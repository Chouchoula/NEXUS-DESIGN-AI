"""
NEXUS DESIGN AI - Agent Task Schemas
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

from api.models.agent_task import AgentType, TaskStatus


class AgentTaskBase(BaseModel):
    """Base agent task schema."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    agent_type: AgentType
    input_data: Optional[Dict[str, Any]] = None
    requires_approval: bool = False


class AgentTaskCreate(AgentTaskBase):
    """Schema for creating an agent task."""
    project_id: UUID
    workflow_id: Optional[UUID] = None


class AgentTaskUpdate(BaseModel):
    """Schema for updating an agent task."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    requires_approval: Optional[bool] = None
    approved: Optional[bool] = None
    rejection_reason: Optional[str] = None


class AgentTaskResponse(AgentTaskBase):
    """Schema for agent task response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    workflow_id: Optional[UUID] = None
    status: TaskStatus
    output_data: Optional[Dict[str, Any]] = None
    model_provider: Optional[str] = None
    model_name: Optional[str] = None
    tokens_used: int = 0
    execution_time: Optional[float] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    requires_approval: bool = False
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None