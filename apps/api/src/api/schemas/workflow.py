"""
NEXUS DESIGN AI - Workflow Schemas
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

from api.models.workflow import WorkflowStatus, WorkflowStepStatus


class WorkflowStepBase(BaseModel):
    """Base workflow step schema."""
    step_number: int
    agent_type: str
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None
    config: Optional[Dict[str, Any]] = None
    requires_approval: bool = False


class WorkflowStepCreate(WorkflowStepBase):
    """Schema for creating a workflow step."""
    pass


class WorkflowStepResponse(WorkflowStepBase):
    """Schema for workflow step response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workflow_id: UUID
    status: WorkflowStepStatus
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    tokens_used: int = 0
    execution_time: Optional[float] = None
    approved: Optional[bool] = None
    approval_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class WorkflowBase(BaseModel):
    """Base workflow schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    workflow_type: str = Field(..., min_length=1, max_length=100)
    steps_definition: List[Dict[str, Any]]


class WorkflowCreate(WorkflowBase):
    """Schema for creating a workflow."""
    project_id: UUID


class WorkflowUpdate(BaseModel):
    """Schema for updating a workflow."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[WorkflowStatus] = None
    current_step: Optional[int] = None
    error_message: Optional[str] = None


class WorkflowResponse(WorkflowBase):
    """Schema for workflow response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    status: WorkflowStatus
    current_step: int = 0
    total_tokens: int = 0
    total_cost: Optional[float] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    steps: List[WorkflowStepResponse] = []


class WorkflowListResponse(BaseModel):
    """Schema for paginated workflow list."""
    items: List[WorkflowResponse]
    total: int
    page: int
    page_size: int
    total_pages: int