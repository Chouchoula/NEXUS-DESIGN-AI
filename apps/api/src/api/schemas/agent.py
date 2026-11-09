"""
NEXUS DESIGN AI - Agent Communication Schemas
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime


class AgentMessage(BaseModel):
    """Message sent to/from agents."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    workflow_id: Optional[UUID] = None
    task_id: Optional[UUID] = None
    from_agent: str
    to_agent: str
    message_type: str  # request, response, notification, approval_request
    content: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime


class AgentRequest(BaseModel):
    """Request sent to an agent."""
    project_id: UUID
    task_id: Optional[UUID] = None
    agent_type: str
    action: str
    payload: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None
    requires_approval: bool = False


class AgentResponse(BaseModel):
    """Response from an agent."""
    task_id: Optional[UUID] = None
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    tokens_used: int = 0
    execution_time: float = 0.0
    requires_approval: bool = False
    approval_payload: Optional[Dict[str, Any]] = None


class AgentStatus(BaseModel):
    """Current status of an agent."""
    agent_type: str
    status: str  # idle, running, waiting, error
    current_task_id: Optional[UUID] = None
    last_activity: Optional[datetime] = None
    total_tasks_completed: int = 0
    total_tokens_used: int = 0