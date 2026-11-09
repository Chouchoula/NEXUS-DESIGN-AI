"""
NEXUS DESIGN AI - Base Agent Class
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from uuid import UUID
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

from api.config import settings
from api.schemas.agent import AgentRequest, AgentResponse


class AgentStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    WAITING = "waiting"
    ERROR = "error"
    COMPLETED = "completed"


@dataclass
class AgentContext:
    """Context passed between agents in a workflow."""
    project_id: UUID
    workflow_id: Optional[UUID] = None
    task_id: Optional[UUID] = None
    previous_outputs: Dict[str, Any] = field(default_factory=dict)
    shared_data: Dict[str, Any] = field(default_factory=dict)
    token_budget: Optional[int] = None
    tokens_used: int = 0


class BaseAgent(ABC):
    """Base class for all NEXUS DESIGN AI agents."""

    def __init__(
        self,
        agent_type: str,
        name: str,
        description: str,
        system_prompt: str,
        tools: Optional[List[str]] = None,
        requires_approval: bool = False,
    ):
        self.agent_type = agent_type
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.requires_approval = requires_approval
        self.status = AgentStatus.IDLE
        self.current_task_id: Optional[UUID] = None
        self.total_tasks_completed = 0
        self.total_tokens_used = 0
        self.last_activity: Optional[datetime] = None

    @abstractmethod
    async def execute(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Execute the agent's primary task."""
        pass

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities."""
        pass

    async def validate_input(self, request: AgentRequest) -> bool:
        """Validate input before execution. Override in subclasses."""
        return True

    async def pre_execute(self, request: AgentRequest, context: AgentContext) -> None:
        """Pre-execution hook. Override in subclasses."""
        self.status = AgentStatus.RUNNING
        self.current_task_id = request.task_id
        self.last_activity = datetime.utcnow()

    async def post_execute(self, response: AgentResponse, context: AgentContext) -> None:
        """Post-execution hook. Override in subclasses."""
        self.status = AgentStatus.COMPLETED if response.success else AgentStatus.ERROR
        self.total_tasks_completed += 1
        self.total_tokens_used += response.tokens_used
        context.tokens_used += response.tokens_used
        self.current_task_id = None
        self.last_activity = datetime.utcnow()

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "agent_type": self.agent_type,
            "name": self.name,
            "status": self.status.value,
            "current_task_id": str(self.current_task_id) if self.current_task_id else None,
            "total_tasks_completed": self.total_tasks_completed,
            "total_tokens_used": self.total_tokens_used,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "tools": self.tools,
            "requires_approval": self.requires_approval,
        }

    def reset(self) -> None:
        """Reset agent state."""
        self.status = AgentStatus.IDLE
        self.current_task_id = None

    def estimate_tokens(self, request: AgentRequest) -> int:
        """Estimate token usage for a request. Override for accuracy."""
        # Rough estimation based on prompt size
        prompt_size = len(str(request.payload)) + len(self.system_prompt)
        return min(prompt_size // 4, settings.MAX_TOKENS_PER_REQUEST)