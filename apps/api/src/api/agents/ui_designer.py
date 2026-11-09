"""
NEXUS DESIGN AI - UI Designer Agent
"""

from typing import Dict, Any, List
from uuid import UUID

from api.agents.base import BaseAgent, AgentContext
from api.schemas.agent import AgentRequest, AgentResponse


class UIDesignerAgent(BaseAgent):
    """Master of visual interface design, design systems, and component architecture."""

    def __init__(self):
        with open("api/agents/prompts/ui_designer.md", "r") as f:
            system_prompt = f.read()

        super().__init__(
            agent_type="ui_designer",
            name="UI Designer",
            description="High-fidelity interface design, design systems, components, and Figma integration",
            system_prompt=system_prompt,
            tools=[
                "create_design_tokens",
                "design_component",
                "compose_screen",
                "create_responsive_variants",
                "design_states",
                "figma_create_components",
                "figma_create_prototype",
                "export_assets",
                "generate_tailwind_config",
                "validate_contrast",
            ],
            requires_approval=True,  # UI design system requires approval
        )

    def get_capabilities(self) -> List[str]:
        return [
            "design_system_construction",
            "component_library_design",
            "screen_design",
            "responsive_design",
            "state_design",
            "figma_integration",
            "design_specification",
            "asset_preparation",
            "developer_handoff",
        ]

    async def execute(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Execute UI design task."""
        task_type = request.payload.get("task_type", "full_ui")

        if task_type == "full_ui":
            return await self._full_ui_design(request, context)
        elif task_type == "tokens_only":
            return await self._tokens_only(request, context)
        elif task_type == "components_only":
            return await self._components_only(request, context)
        elif task_type == "screens_only":
            return await self._screens_only(request, context)
        elif task_type == "figma_sync":
            return await self._figma_sync(request, context)
        else:
            return AgentResponse(
                success=False,
                error=f"Unknown task type: {task_type}",
            )

    async def _full_ui_design(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Complete UI design phase."""
        art_direction = context.previous_outputs.get("art_direction", {})
        ux_specs = context.previous_outputs.get("ux_design", {})
        project_data = request.payload.get("project_context", {})
        product_type = project_data.get("product_type", "website")

        result = {
            "design_system": await self._build_design_system(art_direction, product_type),
            "components": await self._design_core_components(art_direction, ux_specs),
            "patterns": await self._design_patterns(art_direction, ux_specs),
            "screens": await self._design_key_screens(art_direction, ux_specs, product_type),
            "assets": await self._prepare_assets(art_direction),
            "handoff": await self._prepare_handoff(art_direction, product_type),
        }

        return AgentResponse(
            success=True,
            result=result,
            tokens_used=self.estimate_tokens(request),
            requires_approval=True,
            approval_payload={
                "phase": "ui_design",
                "data": result,
                "prompt": "Review and approve design system and screens before development begins",
            },
        )

    async def _tokens_only(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Design tokens only."""
        art_direction = context.previous_outputs.get("art_direction", {})
        tokens = await self._build_design_system(art_direction, "website")
        return AgentResponse(
            success=True,
            result={"design_system": tokens},
            tokens_used=self.estimate_tokens(request),
        )

    async def _components_only(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Core components only."""
        art_direction = context.previous_outputs.get("art_direction", {})
        ux_specs = context.previous_outputs.get("ux_design", {})
        components = await self._design_core_components(art_direction, ux_specs)
        return AgentResponse(
            success=True,
            result={"components": components},
            tokens_used=self.estimate_tokens(request),
        )

    async def _screens_only(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Screen designs only."""
        art_direction = context.previous_outputs.get("art_direction", {})
        ux_specs = context.previous_outputs.get("ux_design", {})
        product_type = request.payload.get("product_type", "website")
        screens = await self._design_key_screens(art_direction, ux_specs, product_type)
        return AgentResponse(
            success=True,
            result={"screens": screens},
            tokens_used=self.estimate_tokens(request),
        )

    async def _figma_sync(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Sync with Figma."""
        # Would integrate with Figma API/MCP
        return AgentResponse(
            success=True,
            result={"figma": {"file_url": "https://figma.com/file/...", "components_synced": 42}},
            tokens_used=self.estimate_tokens(request),
        )

    async def _build_design_system(self, art_direction: Dict, product_type: str) -> Dict[str, Any]:
        """Build complete design system from art direction."""
        colors = art_direction.get("colors", {})
        typography = art_direction.get("typography", {})
        visual_language = art_direction.get("visual_language", {})
        motion = art_direction.get("motion", {})

        return {
            "version": "1.0.0",
            "tokens": {
                "color": {
                    "primitive": colors,
                    "semantic": self._map_semantic_colors(colors),
                },
                "typography": typography,
                "spacing": visual_language.get("spacing", {"base": "0.25rem", "scale": [0,1,2,3,4,5,6,8,10,12,16,20,24]}),
                "borderRadius": visual_language.get("border_radius", {}),
                "shadow": visual_language.get("shadows", {}),
                "opacity": {"0": "0", "10": "0.1", "20": "0.2", "30": "0.3", "40": "0.4", "50": "0.5", "60": "0.6", "70": "0.7", "80": "0.8", "90": "0.9", "100": "1"},
                "zIndex": {"base": "0", "dropdown": "1000", "sticky": "1100", "modal": "1200", "popover": "1300", "tooltip": "1400", "toast": "1500"},
                "transition": motion,
                "breakpoints": {"sm": "640px", "md": "768px", "lg": "1024px", "xl": "1280px", "2xl": "1536px"},
            },
            "components": [],
            "patterns": [],
            "templates": [],
        }

    def _map_semantic_colors(self, colors: Dict) -> Dict[str, Dict[str, str]]:
        """Map primitive colors to semantic roles."""
        primary = colors.get("primary", {})
        neutral = colors.get("neutral", {})
        semantic = colors.get("semantic", {})

        return {
            "background": {"primary": neutral.get("50", "#FFFFFF"), "secondary": neutral.get("100", "#F5F5F5"), "tertiary": neutral.get("200", "#E5E5E5")},
            "foreground": {"primary": neutral.get("900", "#171717"), "secondary": neutral.get("600", "#525252"), "tertiary": neutral.get("400", "#A3A3A3"), "inverse": "#FFFFFF"},
            "border": {"primary": neutral.get("200", "#E5E5E5"), "secondary": neutral.get("300", "#D4D4D4"), "focus": primary.get("500", "#3B82F6")},
            "brand": {"primary": primary.get("500", "#3B82F6"), "primary_hover": primary.get("600", "#2563EB"), "secondary": colors.get("secondary", {}).get("500", "#64748B")},
            "state": {
                "success": {"bg": semantic.get("success", {}).get("light", "#DCFCE7"), "text": semantic.get("success", {}).get("light", "#166534"), "border": semantic.get("success", {}).get("light", "#86EFAC")},
                "warning": {"bg": semantic.get("warning", {}).get("light", "#FEF3C7"), "text": semantic.get("warning", {}).get("light", "#92400E"), "border": semantic.get("warning", {}).get("light", "#FCD34D")},
                "error": {"bg": semantic.get("error", {}).get("light", "#FEE2E2"), "text": semantic.get("error", {}).get("light", "#991B1B"), "border": semantic.get("error", {}).get("light", "#FCA5A5")},
                "info": {"bg": semantic.get("info", {}).get("light", "#DBEAFE"), "text": semantic.get("info", {}).get("light", "#1E40AF"), "border": semantic.get("info", {}).get("light", "#93C5FD")},
            },
        }

    async def _design_core_components(self, art_direction: Dict, ux_specs: Dict) -> List[Dict[str, Any]]:
        """Design core component library."""
        components = [
            "Button", "IconButton", "ButtonGroup",
            "Input", "Textarea", "Select", "Checkbox", "Radio", "Switch", "Slider",
            "Label", "Hint", "ErrorMessage", "FormField",
            "Card", "CardHeader", "CardContent", "CardFooter",
            "Modal", "Dialog", "Drawer", "Popover", "Tooltip",
            "Dropdown", "Menu", "CommandPalette",
            "Table", "DataGrid", "Column", "Row", "Cell",
            "Tabs", "Accordion", "Stepper",
            "Avatar", "Badge", "Tag", "Chip",
            "Progress", "Spinner", "Skeleton",
            "Alert", "Toast", "Notification",
            "Breadcrumb", "Pagination",
            "Navbar", "Sidebar", "Footer", "Breadcrumbs",
            "Heading", "Text", "Link", "Code", "Blockquote",
            "Container", "Grid", "Flex", "Stack", "Divider",
            "EmptyState", "ErrorBoundary",
        ]

        designed = []
        for name in components:
            designed.append(await self._design_component(name, art_direction, ux_specs))
        return designed

    async def _design_component(self, name: str, art_direction: Dict, ux_specs: Dict) -> Dict[str, Any]:
        """Design a single component."""
        # Component configurations
        configs = {
            "Button": {"category": "action", "variants": ["primary", "secondary", "ghost", "danger", "success"], "sizes": ["xs", "sm", "md", "lg", "xl"], "slots": ["iconStart", "iconEnd", "loadingSpinner"]},
            "Input": {"category": "form", "variants": ["default", "error", "success"], "sizes": ["sm", "md", "lg"], "slots": ["iconStart", "iconEnd"]},
            "Card": {"category": "display", "variants": ["default", "outlined", "elevated"], "sizes": [], "slots": ["header", "content", "footer"]},
            "Modal": {"category": "overlay", "variants": ["default", "confirmation", "form"], "sizes": ["sm", "md", "lg", "xl", "full"], "slots": ["header", "content", "footer"]},
        }
        config = configs.get(name, {"category": "general", "variants": ["default"], "sizes": ["md"], "slots": []})

        return {
            "name": name,
            "category": config["category"],
            "variants": config["variants"],
            "sizes": config["sizes"],
            "states": ["default", "hover", "focus", "active", "disabled", "loading", "error"],
            "slots": config["slots"],
            "props": {k: v[0] if isinstance(v, list) else v for k, v in {"variant": config["variants"], "size": config["sizes"]}.items()},
            "accessibility": {"role": "generic", "keyboard": "Tab/Enter/Space", "aria": "generic"},
            "figma_node_id": f"figma:{name.lower()}",
            "code_ref": f"components/ui/{name.lower()}.tsx",
        }

    async def _design_patterns(self, art_direction: Dict, ux_specs: Dict) -> List[Dict[str, Any]]:
        """Design composite patterns."""
        return [
            {"name": "SearchBar", "components": ["Input", "Button", "Dropdown"], "description": "Search with autocomplete"},
            {"name": "FilterBar", "components": ["Select", "Checkbox", "Button", "Input"], "description": "Multi-filter sidebar"},
            {"name": "DataTable", "components": ["Table", "Pagination", "Select", "Button", "IconButton"], "description": "Sortable, filterable, paginated table"},
            {"name": "FormLayout", "components": ["FormField", "Input", "Select", "Button", "Alert"], "description": "Multi-section form with validation"},
            {"name": "DashboardGrid", "components": ["Grid", "Card", "MetricCard", "Chart"], "description": "Responsive widget grid"},
            {"name": "AuthForms", "components": ["Card", "FormField", "Input", "Button", "Link", "Alert"], "description": "Login, register, reset flows"},
            {"name": "OnboardingFlow", "components": ["Stepper", "Card", "Button", "Illustration"], "description": "Multi-step onboarding"},
            {"name": "SettingsPanels", "components": ["Sidebar", "Tabs", "FormField", "Switch", "Button"], "description": "Categorized settings"},
            {"name": "CommandPalette", "components": ["Modal", "Input", "List", "KeyboardShortcut"], "description": "Command+k palette"},
        ]

    async def _design_key_screens(self, art_direction: Dict, ux_specs: Dict, product_type: str) -> List[Dict[str, Any]]:
        """Design key screens for product type."""
        screens_map = {
            "website": ["Home", "About", "Services", "Contact", "BlogPost", "404"],
            "mobile_app": ["Onboarding", "Home", "DetailView", "ListView", "Profile", "Settings", "Auth"],
            "dashboard": ["Overview", "Analytics", "DataTable", "DetailView", "Settings", "EmptyState", "Auth"],
            "saas": ["Workspace", "ProjectView", "BoardView", "CalendarView", "TeamSettings", "Billing", "Integrations", "Auth"],
            "desktop_app": ["MainWindow", "Preferences", "Wizard", "FileBrowser", "About"],
            "brand_identity": ["LogoSystem", "ColorPalette", "Typography", "Iconography", "Applications", "Guidelines"],
        }
        screens = screens_map.get(product_type, screens_map["website"])

        designed = []
        for screen in screens:
            designed.append(await self._design_screen(screen, art_direction, ux_specs, product_type))
        return designed

    async def _design_screen(self, name: str, art_direction: Dict, ux_specs: Dict, product_type: str) -> Dict[str, Any]:
        """Design a single screen."""
        wireframes = ux_specs.get("wireframes", [])
        wireframe = next((w for w in wireframes if w["screen"] == name), {})

        return {
            "name": name,
            "route": self._get_route(name, product_type),
            "breakpoints": {
                "mobile": {"figma_frame": f"figma:{name.lower()}:mobile", "components": wireframe.get("components", [])},
                "tablet": {"figma_frame": f"figma:{name.lower()}:tablet", "components": wireframe.get("components", [])},
                "desktop": {"figma_frame": f"figma:{name.lower()}:desktop", "components": wireframe.get("components", [])},
            },
            "states": {
                "default": f"figma:{name.lower()}:default",
                "loading": f"figma:{name.lower()}:loading",
                "empty": f"figma:{name.lower()}:empty",
                "error": f"figma:{name.lower()}:error",
            },
            "annotations": self._generate_annotations(name, wireframe),
        }

    def _get_route(self, screen: str, product_type: str) -> str:
        """Get route for screen."""
        route_map = {
            "Home": "/",
            "About": "/about",
            "Services": "/services",
            "Contact": "/contact",
            "BlogPost": "/blog/[slug]",
            "404": "/404",
            "Onboarding": "/onboarding",
            "DetailView": "/detail/[id]",
            "ListView": "/list",
            "Profile": "/profile",
            "Settings": "/settings",
            "Auth": "/auth",
            "Overview": "/dashboard",
            "Analytics": "/dashboard/analytics",
            "DataTable": "/dashboard/data",
            "DetailView": "/dashboard/detail/[id]",
            "Workspace": "/workspace",
            "ProjectView": "/projects/[id]",
            "TeamSettings": "/settings/team",
            "Billing": "/settings/billing",
            "Integrations": "/settings/integrations",
            "MainWindow": "/",
            "Preferences": "/preferences",
            "Wizard": "/wizard",
            "FileBrowser": "/files",
        }
        return route_map.get(screen, f"/{screen.lower()}")

    def _generate_annotations(self, screen: str, wireframe: Dict) -> List[Dict[str, Any]]:
        """Generate developer annotations."""
        return [
            {"element": "Container", "notes": "Max-width 1280px, centered", "redline": "24px horizontal padding"},
            {"element": "Button", "notes": "Primary variant, md size", "redline": "16px gap from adjacent"},
            {"element": "Card", "notes": "Elevated variant, hover shadow", "redline": "24px grid gap"},
        ]

    async def _prepare_assets(self, art_direction: Dict) -> Dict[str, List[Dict[str, Any]]]:
        """Prepare exportable assets."""
        return {
            "icons": [
                {"name": "logo", "figma_node": "figma:logo", "formats": ["svg", "png@2x", "png@3x"]},
                {"name": "favicon", "figma_node": "figma:favicon", "formats": ["ico", "png@1x", "png@2x"]},
            ],
            "illustrations": [
                {"name": "onboarding-1", "figma_node": "figma:illustration:onboarding-1", "formats": ["svg", "png@2x"]},
                {"name": "empty-state", "figma_node": "figma:illustration:empty-state", "formats": ["svg", "png@2x"]},
            ],
            "logos": [
                {"name": "primary", "figma_node": "figma:logo:primary", "formats": ["svg", "png@2x", "png@3x"]},
                {"name": "secondary", "figma_node": "figma:logo:secondary", "formats": ["svg", "png@2x"]},
            ],
        }

    async def _prepare_handoff(self, art_direction: Dict, product_type: str) -> Dict[str, Any]:
        """Prepare developer handoff package."""
        return {
            "tailwind_config": "Generated from design tokens",
            "css_variables": "Generated from color/typography tokens",
            "component_map": {c["name"]: c["code_ref"] for c in await self._design_core_components(art_direction, {})},
            "implementation_notes": [
                "Use CSS variables for theming (light/dark)",
                "All components use class-variance-authority for variants",
                "Framer Motion for animations, respect prefers-reduced-motion",
                "React Hook Form + Zod for forms",
                "React Query for server state",
                "Zustand for client state",
            ],
        }