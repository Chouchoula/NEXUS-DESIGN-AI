"""
NEXUS DESIGN AI - Design Workflow Orchestration
"""

from typing import Dict, Any, List, Optional, TypedDict, Annotated
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from api.agents import (
    OrchestratorAgent,
    ResearchAgent,
    ArtDirectorAgent,
    UIDesignerAgent,
    UXDesignerAgent,
    FrontendEngineerAgent,
    VisualQAAgent,
)
from api.agents.base import AgentContext
from api.schemas.agent import AgentRequest
from api.config import settings


class WorkflowPhase(str, Enum):
    """Workflow phases."""
    ANALYZE = "analyze"
    RESEARCH = "research"
    ART_DIRECTION = "art_direction"
    UX_DESIGN = "ux_design"
    UI_DESIGN = "ui_design"
    HUMAN_APPROVAL_ART = "human_approval_art"
    HUMAN_APPROVAL_UX = "human_approval_ux"
    HUMAN_APPROVAL_UI = "human_approval_ui"
    HUMAN_APPROVAL_DEV = "human_approval_dev"
    FRONTEND_DEVELOPMENT = "frontend_development"
    VISUAL_QA = "visual_qa"
    DELIVERY = "delivery"


class WorkflowState(TypedDict):
    """State for the design workflow."""
    project_id: str
    workflow_id: str
    current_phase: WorkflowPhase
    completed_phases: List[WorkflowPhase]
    pending_approvals: List[Dict[str, Any]]
    agent_outputs: Dict[str, Any]
    project_context: Dict[str, Any]
    token_budget: int
    tokens_used: int
    errors: List[str]
    human_feedback: Optional[Dict[str, Any]]


@dataclass
class DesignWorkflow:
    """Main workflow orchestrator using LangGraph."""

    def __init__(self):
        self.orchestrator = OrchestratorAgent()
        self.research = ResearchAgent()
        self.art_director = ArtDirectorAgent()
        self.ux_designer = UXDesignerAgent()
        self.ui_designer = UIDesignerAgent()
        self.frontend_engineer = FrontendEngineerAgent()
        self.visual_qa = VisualQAAgent()

        self.agents = {
            "orchestrator": self.orchestrator,
            "research": self.research,
            "art_director": self.art_director,
            "ux_designer": self.ux_designer,
            "ui_designer": self.ui_designer,
            "frontend_engineer": self.frontend_engineer,
            "visual_qa": self.visual_qa,
        }

        self.graph = self._build_graph()
        self.checkpointer = MemorySaver()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(WorkflowState)

        # Add nodes for each phase
        workflow.add_node("analyze", self._analyze_phase)
        workflow.add_node("research", self._research_phase)
        workflow.add_node("art_direction", self._art_direction_phase)
        workflow.add_node("human_approval_art", self._human_approval_art_phase)
        workflow.add_node("ux_design", self._ux_design_phase)
        workflow.add_node("human_approval_ux", self._human_approval_ux_phase)
        workflow.add_node("ui_design", self._ui_design_phase)
        workflow.add_node("human_approval_ui", self._human_approval_ui_phase)
        workflow.add_node("frontend_development", self._frontend_development_phase)
        workflow.add_node("human_approval_dev", self._human_approval_dev_phase)
        workflow.add_node("visual_qa", self._visual_qa_phase)
        workflow.add_node("delivery", self._delivery_phase)

        # Define edges
        workflow.set_entry_point("analyze")

        workflow.add_edge("analyze", "research")
        workflow.add_edge("research", "art_direction")
        workflow.add_edge("art_direction", "human_approval_art")
        workflow.add_edge("human_approval_art", "ux_design")
        workflow.add_edge("ux_design", "human_approval_ux")
        workflow.add_edge("human_approval_ux", "ui_design")
        workflow.add_edge("ui_design", "human_approval_ui")
        workflow.add_edge("human_approval_ui", "frontend_development")
        workflow.add_edge("frontend_development", "human_approval_dev")
        workflow.add_edge("human_approval_dev", "visual_qa")
        workflow.add_edge("visual_qa", "delivery")
        workflow.add_edge("delivery", END)

        # Add conditional edges for approval gates
        workflow.add_conditional_edges(
            "human_approval_art",
            self._check_approval,
            {"approved": "ux_design", "rejected": "art_direction", "pending": "human_approval_art"},
        )
        workflow.add_conditional_edges(
            "human_approval_ux",
            self._check_approval,
            {"approved": "ui_design", "rejected": "ux_design", "pending": "human_approval_ux"},
        )
        workflow.add_conditional_edges(
            "human_approval_ui",
            self._check_approval,
            {"approved": "frontend_development", "rejected": "ui_design", "pending": "human_approval_ui"},
        )
        workflow.add_conditional_edges(
            "human_approval_dev",
            self._check_approval,
            {"approved": "visual_qa", "rejected": "frontend_development", "pending": "human_approval_dev"},
        )

        return workflow.compile(checkpointer=self.checkpointer)

    async def _analyze_phase(self, state: WorkflowState) -> WorkflowState:
        """Analyze project and create workflow plan."""
        request = AgentRequest(
            project_id=UUID(state["project_id"]),
            task_id=uuid4(),
            agent_type="orchestrator",
            action="plan",
            payload={
                "project": state["project_context"],
                "token_budget": state["token_budget"],
            },
            context=state["project_context"],
        )

        context = AgentContext(
            project_id=UUID(state["project_id"]),
            workflow_id=UUID(state["workflow_id"]),
            token_budget=state["token_budget"],
            tokens_used=state["tokens_used"],
        )

        response = await self.orchestrator.execute(request, context)

        if response.success:
            state["agent_outputs"]["orchestrator"] = response.result
            state["completed_phases"].append(WorkflowPhase.ANALYZE)
            state["current_phase"] = WorkflowPhase.RESEARCH
            state["tokens_used"] += response.tokens_used
        else:
            state["errors"].append(f"Analysis failed: {response.error}")

        return state

    async def _research_phase(self, state: WorkflowState) -> WorkflowState:
        """Execute research phase."""
        request = AgentRequest(
            project_id=UUID(state["project_id"]),
            task_id=uuid4(),
            agent_type="research",
            action="execute",
            payload={
                "task_type": "full_research",
                "project_context": state["project_context"],
            },
            context=state["project_context"],
        )

        context = AgentContext(
            project_id=UUID(state["project_id"]),
            workflow_id=UUID(state["workflow_id"]),
            previous_outputs=state["agent_outputs"],
            token_budget=state["token_budget"],
            tokens_used=state["tokens_used"],
        )

        response = await self.research.execute(request, context)

        if response.success:
            state["agent_outputs"]["research"] = response.result
            state["completed_phases"].append(WorkflowPhase.RESEARCH)
            state["current_phase"] = WorkflowPhase.ART_DIRECTION
            state["tokens_used"] += response.tokens_used
        else:
            state["errors"].append(f"Research failed: {response.error}")

        return state

    async def _art_direction_phase(self, state: WorkflowState) -> WorkflowState:
        """Execute art direction phase."""
        request = AgentRequest(
            project_id=UUID(state["project_id"]),
            task_id=uuid4(),
            agent_type="art_director",
            action="execute",
            payload={
                "task_type": "full_direction",
                "project_context": state["project_context"],
            },
            context=state["project_context"],
        )

        context = AgentContext(
            project_id=UUID(state["project_id"]),
            workflow_id=UUID(state["workflow_id"]),
            previous_outputs=state["agent_outputs"],
            token_budget=state["token_budget"],
            tokens_used=state["tokens_used"],
        )

        response = await self.art_director.execute(request, context)

        if response.success:
            state["agent_outputs"]["art_direction"] = response.result
            state["completed_phases"].append(WorkflowPhase.ART_DIRECTION)
            state["current_phase"] = WorkflowPhase.HUMAN_APPROVAL_ART
            state["pending_approvals"].append({
                "phase": "art_direction",
                "data": response.result,
                "prompt": response.approval_payload.get("prompt") if response.approval_payload else "Approve art direction?",
                "approval_payload": response.approval_payload,
            })
            state["tokens_used"] += response.tokens_used
        else:
            state["errors"].append(f"Art direction failed: {response.error}")

        return state

    async def _human_approval_art_phase(self, state: WorkflowState) -> WorkflowState:
        """Wait for human approval on art direction."""
        # In real implementation, this would wait for human input
        # For now, simulate approval from context
        feedback = state.get("human_feedback", {})
        if feedback.get("art_direction_approved"):
            state["pending_approvals"] = [p for p in state["pending_approvals"] if p["phase"] != "art_direction"]
        return state

    async def _ux_design_phase(self, state: WorkflowState) -> WorkflowState:
        """Execute UX design phase."""
        request = AgentRequest(
            project_id=UUID(state["project_id"]),
            task_id=uuid4(),
            agent_type="ux_designer",
            action="execute",
            payload={
                "task_type": "full_ux",
                "project_context": state["project_context"],
            },
            context=state["project_context"],
        )

        context = AgentContext(
            project_id=UUID(state["project_id"]),
            workflow_id=UUID(state["workflow_id"]),
            previous_outputs=state["agent_outputs"],
            token_budget=state["token_budget"],
            tokens_used=state["tokens_used"],
        )

        response = await self.ux_designer.execute(request, context)

        if response.success:
            state["agent_outputs"]["ux_design"] = response.result
            state["completed_phases"].append(WorkflowPhase.UX_DESIGN)
            state["current_phase"] = WorkflowPhase.HUMAN_APPROVAL_UX
            state["pending_approvals"].append({
                "phase": "ux_design",
                "data": response.result,
                "prompt": response.approval_payload.get("prompt") if response.approval_payload else "Approve UX design?",
                "approval_payload": response.approval_payload,
            })
            state["tokens_used"] += response.tokens_used
        else:
            state["errors"].append(f"UX design failed: {response.error}")

        return state

    async def _human_approval_ux_phase(self, state: WorkflowState) -> WorkflowState:
        """Wait for human approval on UX design."""
        feedback = state.get("human_feedback", {})
        if feedback.get("ux_design_approved"):
            state["pending_approvals"] = [p for p in state["pending_approvals"] if p["phase"] != "ux_design"]
        return state

    async def _ui_design_phase(self, state: WorkflowState) -> WorkflowState:
        """Execute UI design phase."""
        request = AgentRequest(
            project_id=UUID(state["project_id"]),
            task_id=uuid4(),
            agent_type="ui_designer",
            action="execute",
            payload={
                "task_type": "full_ui",
                "project_context": state["project_context"],
            },
            context=state["project_context"],
        )

        context = AgentContext(
            project_id=UUID(state["project_id"]),
            workflow_id=UUID(state["workflow_id"]),
            previous_outputs=state["agent_outputs"],
            token_budget=state["token_budget"],
            tokens_used=state["tokens_used"],
        )

        response = await self.ui_designer.execute(request, context)

        if response.success:
            state["agent_outputs"]["ui_design"] = response.result
            state["completed_phases"].append(WorkflowPhase.UI_DESIGN)
            state["current_phase"] = WorkflowPhase.HUMAN_APPROVAL_UI
            state["pending_approvals"].append({
                "phase": "ui_design",
                "data": response.result,
                "prompt": response.approval_payload.get("prompt") if response.approval_payload else "Approve UI design?",
                "approval_payload": response.approval_payload,
            })
            state["tokens_used"] += response.tokens_used
        else:
            state["errors"].append(f"UI design failed: {response.error}")

        return state

    async def _human_approval_ui_phase(self, state: WorkflowState) -> WorkflowState:
        """Wait for human approval on UI design."""
        feedback = state.get("human_feedback", {})
        if feedback.get("ui_design_approved"):
            state["pending_approvals"] = [p for p in state["pending_approvals"] if p["phase"] != "ui_design"]
        return state

    async def _frontend_development_phase(self, state: WorkflowState) -> WorkflowState:
        """Execute frontend development phase."""
        request = AgentRequest(
            project_id=UUID(state["project_id"]),
            task_id=uuid4(),
            agent_type="frontend_engineer",
            action="execute",
            payload={
                "task_type": "full_implementation",
                "project_context": state["project_context"],
            },
            context=state["project_context"],
        )

        context = AgentContext(
            project_id=UUID(state["project_id"]),
            workflow_id=UUID(state["workflow_id"]),
            previous_outputs=state["agent_outputs"],
            token_budget=state["token_budget"],
            tokens_used=state["tokens_used"],
        )

        response = await self.frontend_engineer.execute(request, context)

        if response.success:
            state["agent_outputs"]["frontend_development"] = response.result
            state["completed_phases"].append(WorkflowPhase.FRONTEND_DEVELOPMENT)
            state["current_phase"] = WorkflowPhase.HUMAN_APPROVAL_DEV
            state["pending_approvals"].append({
                "phase": "frontend_development",
                "data": response.result,
                "prompt": response.approval_payload.get("prompt") if response.approval_payload else "Approve implementation?",
                "approval_payload": response.approval_payload,
            })
            state["tokens_used"] += response.tokens_used
        else:
            state["errors"].append(f"Frontend development failed: {response.error}")

        return state

    async def _human_approval_dev_phase(self, state: WorkflowState) -> WorkflowState:
        """Wait for human approval on development."""
        feedback = state.get("human_feedback", {})
        if feedback.get("frontend_development_approved"):
            state["pending_approvals"] = [p for p in state["pending_approvals"] if p["phase"] != "frontend_development"]
        return state

    async def _visual_qa_phase(self, state: WorkflowState) -> WorkflowState:
        """Execute Visual QA phase."""
        request = AgentRequest(
            project_id=UUID(state["project_id"]),
            task_id=uuid4(),
            agent_type="visual_qa",
            action="execute",
            payload={
                "task_type": "full_qa",
                "project_context": state["project_context"],
                "app_url": state["project_context"].get("app_url", "http://localhost:3000"),
            },
            context=state["project_context"],
        )

        context = AgentContext(
            project_id=UUID(state["project_id"]),
            workflow_id=UUID(state["workflow_id"]),
            previous_outputs=state["agent_outputs"],
            token_budget=state["token_budget"],
            tokens_used=state["tokens_used"],
        )

        response = await self.visual_qa.execute(request, context)

        if response.success:
            state["agent_outputs"]["visual_qa"] = response.result
            state["completed_phases"].append(WorkflowPhase.VISUAL_QA)
            state["current_phase"] = WorkflowPhase.DELIVERY
            state["tokens_used"] += response.tokens_used
        else:
            state["errors"].append(f"Visual QA failed: {response.error}")

        return state

    async def _delivery_phase(self, state: WorkflowState) -> WorkflowState:
        """Final delivery phase."""
        request = AgentRequest(
            project_id=UUID(state["project_id"]),
            task_id=uuid4(),
            agent_type="orchestrator",
            action="complete",
            payload={
                "deliverables": state["agent_outputs"],
                "summary": "Design-to-development workflow completed",
            },
            context=state["project_context"],
        )

        context = AgentContext(
            project_id=UUID(state["project_id"]),
            workflow_id=UUID(state["workflow_id"]),
            previous_outputs=state["agent_outputs"],
            token_budget=state["token_budget"],
            tokens_used=state["tokens_used"],
        )

        response = await self.orchestrator.execute(request, context)

        if response.success:
            state["agent_outputs"]["delivery"] = response.result
            state["completed_phases"].append(WorkflowPhase.DELIVERY)
            state["current_phase"] = WorkflowPhase.DELIVERY
            state["tokens_used"] += response.tokens_used
        else:
            state["errors"].append(f"Delivery failed: {response.error}")

        return state

    def _check_approval(self, state: WorkflowState) -> str:
        """Check if human approval was given."""
        feedback = state.get("human_feedback", {})
        current_phase = state["current_phase"]

        approval_map = {
            WorkflowPhase.HUMAN_APPROVAL_ART: "art_direction_approved",
            WorkflowPhase.HUMAN_APPROVAL_UX: "ux_design_approved",
            WorkflowPhase.HUMAN_APPROVAL_UI: "ui_design_approved",
            WorkflowPhase.HUMAN_APPROVAL_DEV: "frontend_development_approved",
        }

        key = approval_map.get(current_phase)
        if key and feedback.get(key):
            return "approved"
        elif key is not None and feedback.get(key) is False:
            return "rejected"
        return "pending"

    async def run(
        self,
        project_id: UUID,
        workflow_id: UUID,
        project_context: Dict[str, Any],
        token_budget: int = None,
    ) -> Dict[str, Any]:
        """Run the complete workflow."""
        initial_state: WorkflowState = {
            "project_id": str(project_id),
            "workflow_id": str(workflow_id),
            "current_phase": WorkflowPhase.ANALYZE,
            "completed_phases": [],
            "pending_approvals": [],
            "agent_outputs": {},
            "project_context": project_context,
            "token_budget": token_budget or settings.TOTAL_TOKEN_BUDGET or 100000,
            "tokens_used": 0,
            "errors": [],
            "human_feedback": {},
        }

        config = {"configurable": {"thread_id": str(workflow_id)}}
        final_state = await self.graph.ainvoke(initial_state, config)

        return {
            "workflow_id": str(workflow_id),
            "project_id": str(project_id),
            "final_phase": final_state["current_phase"],
            "completed_phases": final_state["completed_phases"],
            "agent_outputs": final_state["agent_outputs"],
            "tokens_used": final_state["tokens_used"],
            "token_budget": final_state["token_budget"],
            "errors": final_state["errors"],
            "pending_approvals": final_state["pending_approvals"],
        }

    async def resume_with_feedback(
        self,
        workflow_id: UUID,
        feedback: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Resume workflow with human feedback."""
        config = {"configurable": {"thread_id": str(workflow_id)}}
        state = await self.graph.aget_state(config)

        if state.values:
            state.values["human_feedback"] = feedback
            final_state = await self.graph.ainvoke(state.values, config)
            return {
                "workflow_id": str(workflow_id),
                "final_phase": final_state["current_phase"],
                "completed_phases": final_state["completed_phases"],
                "agent_outputs": final_state["agent_outputs"],
                "tokens_used": final_state["tokens_used"],
                "errors": final_state["errors"],
            }
        return {"error": "Workflow not found"}


def create_design_workflow() -> DesignWorkflow:
    """Factory function to create a design workflow."""
    return DesignWorkflow()