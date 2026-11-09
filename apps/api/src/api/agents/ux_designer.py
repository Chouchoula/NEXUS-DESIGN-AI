"""
NEXUS DESIGN AI - UX Designer Agent
"""

from typing import Dict, Any, List
from uuid import UUID

from api.agents.base import BaseAgent, AgentContext
from api.schemas.agent import AgentRequest, AgentResponse


class UXDesignerAgent(BaseAgent):
    """Expert in information architecture, user flows, interaction design, and cognitive ergonomics."""

    def __init__(self):
        with open("api/agents/prompts/ux_designer.md", "r") as f:
            system_prompt = f.read()

        super().__init__(
            agent_type="ux_designer",
            name="UX Designer",
            description="Information architecture, user flows, wireframes, and interaction specifications",
            system_prompt=system_prompt,
            tools=[
                "create_sitemap",
                "design_user_flow",
                "create_wireframe",
                "define_interaction_patterns",
                "check_accessibility",
                "apply_cognitive_principles",
                "export_ux_specs",
            ],
            requires_approval=True,  # UX architecture requires approval
        )

    def get_capabilities(self) -> List[str]:
        return [
            "user_research_synthesis",
            "information_architecture",
            "user_flow_design",
            "wireframing",
            "interaction_design",
            "accessibility_strategy",
            "cognitive_ergonomics",
            "usability_heuristics",
        ]

    async def execute(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Execute UX design task."""
        task_type = request.payload.get("task_type", "full_ux")

        if task_type == "full_ux":
            return await self._full_ux_design(request, context)
        elif task_type == "architecture_only":
            return await self._architecture_only(request, context)
        elif task_type == "flows_only":
            return await self._flows_only(request, context)
        elif task_type == "wireframes_only":
            return await self._wireframes_only(request, context)
        elif task_type == "accessibility_audit":
            return await self._accessibility_audit(request, context)
        else:
            return AgentResponse(
                success=False,
                error=f"Unknown task type: {task_type}",
            )

    async def _full_ux_design(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Complete UX design phase."""
        art_direction = context.previous_outputs.get("art_direction", {})
        research_data = context.previous_outputs.get("research", {})
        project_data = request.payload.get("project_context", {})
        product_type = project_data.get("product_type", "website")

        result = {
            "strategy": await self._define_strategy(research_data, project_data),
            "information_architecture": await self._design_architecture(product_type, project_data),
            "user_flows": await self._design_user_flows(product_type, project_data),
            "wireframes": await self._create_key_wireframes(product_type, art_direction),
            "interactions": await self._define_interactions(product_type, art_direction),
            "accessibility": await self._define_accessibility_specs(product_type),
            "handoff_notes": self._generate_handoff_notes(product_type),
        }

        return AgentResponse(
            success=True,
            result=result,
            tokens_used=self.estimate_tokens(request),
            requires_approval=True,
            approval_payload={
                "phase": "ux_design",
                "data": result,
                "prompt": "Review and approve UX architecture and user flows before UI design begins",
            },
        )

    async def _architecture_only(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Information architecture only."""
        product_type = request.payload.get("product_type", "website")
        arch = await self._design_architecture(product_type, request.payload.get("project_context", {}))
        return AgentResponse(
            success=True,
            result={"information_architecture": arch},
            tokens_used=self.estimate_tokens(request),
        )

    async def _flows_only(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """User flows only."""
        product_type = request.payload.get("product_type", "website")
        flows = await self._design_user_flows(product_type, request.payload.get("project_context", {}))
        return AgentResponse(
            success=True,
            result={"user_flows": flows},
            tokens_used=self.estimate_tokens(request),
        )

    async def _wireframes_only(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Wireframes only."""
        product_type = request.payload.get("product_type", "website")
        art_direction = context.previous_outputs.get("art_direction", {})
        wireframes = await self._create_key_wireframes(product_type, art_direction)
        return AgentResponse(
            success=True,
            result={"wireframes": wireframes},
            tokens_used=self.estimate_tokens(request),
        )

    async def _accessibility_audit(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Accessibility specification only."""
        product_type = request.payload.get("product_type", "website")
        specs = await self._define_accessibility_specs(product_type)
        return AgentResponse(
            success=True,
            result={"accessibility": specs},
            tokens_used=self.estimate_tokens(request),
        )

    async def _define_strategy(self, research: Dict, project: Dict) -> Dict[str, Any]:
        """Define UX strategy."""
        return {
            "personas": research.get("domain_profile", {}).get("user_personas", [
                {"name": "Primary User", "goals": ["Efficiency"], "pain_points": ["Complexity"], "context": "Daily work"}
            ]),
            "jobs_to_be_done": [
                "When I need to accomplish a task, I want a clear path, so I can complete it quickly",
                "When I encounter an error, I want clear guidance, so I can recover without frustration",
            ],
            "success_metrics": {
                "task_completion_rate": "> 90%",
                "time_to_complete": "< 2 min for primary tasks",
                "error_rate": "< 2%",
                "satisfaction": "> 4.5/5",
            },
            "experience_principles": [
                "Clarity over cleverness",
                "Consistent patterns reduce learning",
                "Feedback for every action",
                "Sensible defaults, easy customization",
                "Accessible by default",
            ],
        }

    async def _design_architecture(self, product_type: str, project: Dict) -> Dict[str, Any]:
        """Design information architecture."""
        arch_map = {
            "website": {
                "site_map": {
                    "Home": {},
                    "About": {},
                    "Services": {"Service 1": {}, "Service 2": {}},
                    "Blog": {"Category": {"Article": {}}},
                    "Contact": {},
                },
                "navigation": {
                    "global": ["Home", "Services", "Blog", "Contact"],
                    "utility": ["Login", "Sign Up"],
                },
            },
            "mobile_app": {
                "site_map": {
                    "Onboarding": {"Welcome": {}, "Permissions": {}, "Setup": {}},
                    "Home": {"Feed": {}, "Search": {}, "Notifications": {}},
                    "Profile": {"Settings": {}, "Account": {}, "Help": {}},
                },
                "navigation": {
                    "global": ["Home", "Search", "Notifications", "Profile"],
                    "tabs": 4,
                },
            },
            "dashboard": {
                "site_map": {
                    "Overview": {},
                    "Analytics": {"Reports": {}, "Custom": {}},
                    "Data Management": {"Table": {}, "Detail": {}, "Import": {}},
                    "Settings": {"Team": {}, "Billing": {}, "Integrations": {}},
                },
                "navigation": {
                    "global": ["Overview", "Analytics", "Data", "Settings"],
                    "sidebar": True,
                },
            },
            "saas": {
                "site_map": {
                    "Workspace": {"Projects": {}, "Team": {}, "Activity": {}},
                    "Project View": {"Tasks": {}, "Board": {}, "Calendar": {}},
                    "Settings": {"Profile": {}, "Billing": {}, "Integrations": {}},
                },
                "navigation": {
                    "global": ["Workspace", "Projects", "Settings"],
                    "contextual": True,
                },
            },
        }
        return arch_map.get(product_type, arch_map["website"])

    async def _design_user_flows(self, product_type: str, project: Dict) -> List[Dict[str, Any]]:
        """Design user flows."""
        flows_map = {
            "website": [
                {"name": "Contact Inquiry", "trigger": "User visits Contact page", "steps": [
                    {"screen": "Contact Form", "action": "Fill and submit", "decision": "Valid?"},
                    {"screen": "Confirmation", "action": "Show success", "result": "Email sent"},
                ]},
                {"name": "Service Discovery", "trigger": "User lands on Home", "steps": [
                    {"screen": "Hero", "action": "Read value prop", "decision": "Interested?"},
                    {"screen": "Services", "action": "Browse services", "decision": "Select one"},
                    {"screen": "Service Detail", "action": "Read details", "result": "Contact/CTA"},
                ]},
            ],
            "mobile_app": [
                {"name": "Onboarding", "trigger": "First app launch", "steps": [
                    {"screen": "Welcome", "action": "Swipe through", "decision": "Continue?"},
                    {"screen": "Permissions", "action": "Grant access", "decision": "Granted?"},
                    {"screen": "Setup", "action": "Configure preferences", "result": "Home screen"},
                ]},
            ],
            "dashboard": [
                {"name": "Data Analysis", "trigger": "User opens Analytics", "steps": [
                    {"screen": "Overview", "action": "Scan metrics", "decision": "Drill down?"},
                    {"screen": "Detail Report", "action": "Filter/Explore", "decision": "Export?"},
                    {"screen": "Export", "action": "Download/Share", "result": "File saved"},
                ]},
            ],
        }
        return flows_map.get(product_type, flows_map["website"])

    async def _create_key_wireframes(self, product_type: str, art_direction: Dict) -> List[Dict[str, Any]]:
        """Create key wireframes."""
        screens_map = {
            "website": ["Home", "About", "Services", "Contact", "Blog Post"],
            "mobile_app": ["Onboarding", "Home", "Detail", "Profile", "Settings"],
            "dashboard": ["Overview", "Data Table", "Detail View", "Settings", "Empty State"],
            "saas": ["Workspace", "Project View", "Team", "Billing", "Settings"],
        }
        screens = screens_map.get(product_type, screens_map["website"])

        wireframes = []
        for screen in screens:
            wireframes.append({
                "screen": screen,
                "breakpoints": {
                    "mobile": {"layout": ["Header", "Content", "Footer"], "annotations": ["Stack vertically"]},
                    "tablet": {"layout": ["Header", "Sidebar", "Content"], "annotations": ["Collapsible sidebar"]},
                    "desktop": {"layout": ["Header", "Sidebar", "Content", "Footer"], "annotations": ["Full layout"]},
                },
                "components": self._get_screen_components(screen, product_type),
                "content_priority": self._get_content_priority(screen),
            })
        return wireframes

    def _get_screen_components(self, screen: str, product_type: str) -> List[str]:
        """Get components for a screen."""
        component_map = {
            "Home": ["Hero", "FeatureGrid", "Testimonials", "CTA", "Footer"],
            "Dashboard": ["Header", "Sidebar", "MetricCard", "Chart", "DataTable", "ActivityFeed"],
            "Profile": ["Header", "Avatar", "FormField", "Tabs", "Button"],
            "Settings": ["Sidebar", "Section", "FormField", "Switch", "Button"],
        }
        return component_map.get(screen, ["Container", "Heading", "Text", "Button"])

    def _get_content_priority(self, screen: str) -> List[str]:
        """Get content priority for a screen."""
        priority_map = {
            "Home": ["Value Proposition", "Primary CTA", "Features", "Social Proof"],
            "Dashboard": ["Key Metrics", "Primary Actions", "Recent Activity", "Navigation"],
            "Profile": ["User Info", "Primary Actions", "Preferences", "Account Actions"],
        }
        return priority_map.get(screen, ["Primary Content", "Secondary Content", "Actions"])

    async def _define_interactions(self, product_type: str, art_direction: Dict) -> Dict[str, Any]:
        """Define interaction specifications."""
        return {
            "components": {
                "Button": {"states": ["default", "hover", "focus", "active", "disabled", "loading"], "keyboard": "Enter/Space", "aria": "button"},
                "Input": {"states": ["default", "focus", "error", "disabled"], "keyboard": "Type", "aria": "textbox"},
                "Modal": {"focus_trap": True, "close_on_escape": True, "restore_focus": True, "aria": "dialog"},
                "Dropdown": {"keyboard": "Arrow keys, Enter, Escape", "aria": "listbox"},
                "Tabs": {"keyboard": "Arrow keys, Home, End", "aria": "tablist"},
            },
            "patterns": {
                "form_validation": "Inline on blur, summary on submit, aria-describedby for errors",
                "data_loading": "Skeleton → Content, error retry with announcement",
                "navigation": "Breadcrumbs, back button, keyboard shortcuts (g+h for home)",
                "toast": "aria-live=polite, auto-dismiss 5s, keyboard dismissible",
            },
            "gestures": {
                "swipe": "Horizontal for tabs/carousels, vertical for dismiss",
                "pull_to_refresh": "On list views",
                "long_press": "Context menus on data rows",
            },
        }

    async def _define_accessibility_specs(self, product_type: str) -> Dict[str, Any]:
        """Define accessibility specifications."""
        return {
            "wcag_level": "AA",
            "contrast_verified": True,
            "focus_indicators": "Custom, 3px solid outline, brand color, 2px offset",
            "keyboard_navigation": "Full support, logical tab order, skip links",
            "screen_reader": "ARIA labels on all interactive, landmarks, live regions for dynamic content",
            "motion_reduction": "Respects prefers-reduced-motion, disables non-essential animations",
            "touch_targets": "Minimum 44x44pt, 8px spacing between targets",
            "heading_hierarchy": "Single h1 per page, sequential h2-h6",
            "form_accessibility": "Explicit labels, required indicators, error associations",
            "color_independence": "No info conveyed by color alone",
            "zoom_support": "Functional at 200% zoom, no horizontal scroll at 320px",
        }

    def _generate_handoff_notes(self, product_type: str) -> List[str]:
        """Generate handoff notes for UI Designer."""
        return [
            f"All wireframes use {product_type} standard patterns",
            "Responsive breakpoints: 320, 768, 1024, 1440",
            "Touch targets meet 44x44pt minimum",
            "Focus indicators must use brand color from art direction",
            "Loading states required for all async actions",
            "Empty states designed for all data-driven screens",
            "Error states follow inline + toast pattern",
            "All forms use native validation + custom messages",
        ]