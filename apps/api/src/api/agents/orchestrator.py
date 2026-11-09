"""
NEXUS DESIGN AI - Orchestrator Agent
"""

from typing import Dict, Any, List, Optional
from uuid import UUID
from datetime import datetime

from api.agents.base import BaseAgent, AgentContext, AgentStatus
from api.schemas.agent import AgentRequest, AgentResponse
from api.config import settings


class OrchestratorAgent(BaseAgent):
    """Central orchestrator coordinating all specialized agents."""

    def __init__(self):
        # Load system prompt from file
        with open("api/agents/prompts/orchestrator.md", "r") as f:
            system_prompt = f.read()

        super().__init__(
            agent_type="orchestrator",
            name="NEXUS Orchestrator",
            description="Central coordinator for the design-to-development workflow",
            system_prompt=system_prompt,
            tools=[
                "create_workflow",
                "delegate_to_agent",
                "get_agent_result",
                "request_human_approval",
                "update_project_status",
                "log_decision",
                "check_token_budget",
            ],
            requires_approval=False,
        )

        # Workflow templates per product type
        self.workflow_templates = {
            "website": [
                "research",
                "art_direction",
                "ux_design",
                "ui_design",
                "human_approval_ui",
                "frontend_development",
                "visual_qa",
                "delivery",
            ],
            "mobile_app": [
                "research",
                "art_direction",
                "ux_design",
                "ui_design",
                "human_approval_ui",
                "frontend_development",
                "visual_qa",
                "delivery",
            ],
            "dashboard": [
                "research",
                "art_direction",
                "ux_design",
                "ui_design",
                "human_approval_ui",
                "frontend_development",
                "visual_qa",
                "delivery",
            ],
            "saas": [
                "research",
                "art_direction",
                "ux_design",
                "ui_design",
                "human_approval_ui",
                "frontend_development",
                "visual_qa",
                "delivery",
            ],
            "desktop_app": [
                "research",
                "art_direction",
                "ux_design",
                "ui_design",
                "human_approval_ui",
                "frontend_development",
                "visual_qa",
                "delivery",
            ],
            "brand_identity": [
                "research",
                "art_direction",
                "human_approval_art",
                "ui_design",
                "human_approval_ui",
                "delivery",
            ],
        }

        # Approval gates (phases requiring human sign-off)
        self.approval_gates = {
            "art_direction": "Approve artistic direction before UI design",
            "ux_design": "Approve UX architecture before UI design",
            "ui_design": "Approve design system and screens before development",
            "frontend_development": "Approve implementation before QA",
        }

    def get_capabilities(self) -> List[str]:
        return [
            "workflow_planning",
            "agent_coordination",
            "approval_management",
            "token_budget_tracking",
            "project_status_tracking",
            "decision_logging",
            "escalation_handling",
        ]

    async def execute(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Execute orchestrator action based on request."""
        action = request.payload.get("action", "plan")

        if action == "plan":
            return await self._plan_workflow(request, context)
        elif action == "delegate":
            return await self._delegate_task(request, context)
        elif action == "check_status":
            return await self._check_workflow_status(request, context)
        elif action == "request_approval":
            return await self._request_approval(request, context)
        elif action == "complete":
            return await self._complete_workflow(request, context)
        else:
            return AgentResponse(
                success=False,
                error=f"Unknown action: {action}",
            )

    async def _plan_workflow(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Create workflow plan for a project."""
        project_data = request.payload.get("project", {})
        product_type = project_data.get("product_type", "website")
        complexity = project_data.get("complexity", "standard")

        # Get template
        template = self.workflow_templates.get(product_type, self.workflow_templates["website"])

        # Adjust for complexity
        if complexity == "simple":
            # Remove some optional phases
            template = [s for s in template if s not in ["human_approval_art"]]
        elif complexity == "complex":
            # Add extra validation phases
            pass  # Keep all phases

        # Build workflow steps
        steps = []
        for i, step_name in enumerate(template):
            step = {
                "step_number": i + 1,
                "name": step_name.replace("_", " ").title(),
                "agent_type": self._step_to_agent(step_name),
                "requires_approval": step_name in self.approval_gates,
                "approval_prompt": self.approval_gates.get(step_name),
                "config": self._get_step_config(step_name, project_data),
            }
            steps.append(step)

        # Estimate token budget
        estimated_tokens = self._estimate_workflow_tokens(steps, complexity)

        workflow_plan = {
            "project_id": str(context.project_id),
            "workflow_type": f"full_design_{product_type}",
            "steps": steps,
            "estimated_tokens": estimated_tokens,
            "token_budget": request.payload.get("token_budget", settings.TOTAL_TOKEN_BUDGET),
            "approval_gates": [s for s in template if s in self.approval_gates],
            "created_at": datetime.utcnow().isoformat(),
        }

        return AgentResponse(
            success=True,
            result={
                "action": "workflow_created",
                "workflow_plan": workflow_plan,
                "next_agent": "research" if not workflow_plan["steps"][0].get("requires_approval") else None,
                "approval_required": workflow_plan["steps"][0].get("requires_approval", False),
                "approval_prompt": workflow_plan["steps"][0].get("approval_prompt"),
            },
            tokens_used=self.estimate_tokens(request),
        )

    async def _delegate_task(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Delegate task to specialized agent."""
        target_agent = request.payload.get("target_agent")
        task_payload = request.payload.get("task_payload", {})

        # Add context to payload
        task_payload["project_context"] = {
            "project_id": str(context.project_id),
            "workflow_id": str(context.workflow_id) if context.workflow_id else None,
            "previous_outputs": context.previous_outputs,
        }

        return AgentResponse(
            success=True,
            result={
                "action": "delegate",
                "target_agent": target_agent,
                "task_payload": task_payload,
                "requires_approval": False,
            },
            tokens_used=self.estimate_tokens(request),
        )

    async def _check_workflow_status(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Check current workflow status."""
        return AgentResponse(
            success=True,
            result={
                "action": "status",
                "workflow_id": str(context.workflow_id) if context.workflow_id else None,
                "current_phase": context.shared_data.get("current_phase", "unknown"),
                "completed_steps": context.shared_data.get("completed_steps", []),
                "pending_approvals": context.shared_data.get("pending_approvals", []),
                "tokens_used": context.tokens_used,
                "token_budget": context.token_budget,
            },
            tokens_used=self.estimate_tokens(request),
        )

    async def _request_approval(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Request human approval for a phase."""
        phase = request.payload.get("phase")
        prompt = request.payload.get("prompt", f"Approve {phase}?")
        data = request.payload.get("data", {})

        return AgentResponse(
            success=True,
            result={
                "action": "request_approval",
                "phase": phase,
                "prompt": prompt,
                "data": data,
                "requires_approval": True,
                "approval_payload": {
                    "phase": phase,
                    "data": data,
                },
            },
            tokens_used=self.estimate_tokens(request),
            requires_approval=True,
            approval_payload={"phase": phase, "data": data},
        )

    async def _complete_workflow(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Mark workflow as complete."""
        return AgentResponse(
            success=True,
            result={
                "action": "complete",
                "workflow_id": str(context.workflow_id) if context.workflow_id else None,
                "deliverables": request.payload.get("deliverables", {}),
                "summary": request.payload.get("summary", "Workflow completed successfully"),
            },
            tokens_used=self.estimate_tokens(request),
        )

    def _step_to_agent(self, step_name: str) -> str:
        """Map workflow step to agent type."""
        mapping = {
            "research": "research",
            "art_direction": "art_director",
            "ux_design": "ux_designer",
            "ui_design": "ui_designer",
            "frontend_development": "frontend_engineer",
            "visual_qa": "visual_qa",
            "delivery": "orchestrator",
            "human_approval_art": "orchestrator",
            "human_approval_ux": "orchestrator",
            "human_approval_ui": "orchestrator",
            "human_approval_dev": "orchestrator",
        }
        return mapping.get(step_name, "orchestrator")

    def _get_step_config(self, step_name: str, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get configuration for a workflow step."""
        configs = {
            "research": {
                "min_benchmarks": 5,
                "sources": ["figma", "dribbble", "behance", "awwwards", "unsplash", "iconify"],
                "include_trends": True,
            },
            "art_direction": {
                "directions_count": 3,
                "include_motion": True,
                "accessibility_level": "AA",
            },
            "ux_design": {
                "personas_count": 3,
                "flows_count": 5,
                "wireframes_detail": "medium",
            },
            "ui_design": {
                "design_system": True,
                "components_detail": "full",
                "responsive_breakpoints": 5,
            },
            "frontend_development": {
                "framework": "nextjs",
                "styling": "tailwind",
                "animations": "framer_motion",
                "testing": "playwright",
            },
            "visual_qa": {
                "browsers": ["chromium", "firefox", "webkit"],
                "devices": ["mobile", "tablet", "desktop"],
                "accessibility_level": "AA",
                "performance_threshold": 90,
            },
        }
        return configs.get(step_name, {})

    def _estimate_workflow_tokens(self, steps: List[Dict], complexity: str) -> int:
        """Estimate total tokens for workflow."""
        base_tokens = {
            "research": 15000,
            "art_direction": 12000,
            "ux_design": 18000,
            "ui_design": 25000,
            "frontend_development": 30000,
            "visual_qa": 10000,
            "delivery": 2000,
        }

        total = sum(base_tokens.get(s["agent_type"], 5000) for s in steps)

        # Complexity multiplier
        multipliers = {"simple": 0.7, "standard": 1.0, "complex": 1.5}
        return int(total * multipliers.get(complexity, 1.0))