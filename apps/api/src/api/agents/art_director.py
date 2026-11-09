"""
NEXUS DESIGN AI - Art Director Agent
"""

from typing import Dict, Any, List
from uuid import UUID

from api.agents.base import BaseAgent, AgentContext
from api.schemas.agent import AgentRequest, AgentResponse


class ArtDirectorAgent(BaseAgent):
    """Master of visual identity, color theory, typography, and brand expression."""

    def __init__(self):
        with open("api/agents/prompts/art_director.md", "r") as f:
            system_prompt = f.read()

        super().__init__(
            agent_type="art_director",
            name="Art Director",
            description="Visual identity, color systems, typography, and artistic direction",
            system_prompt=system_prompt,
            tools=[
                "generate_color_palette",
                "check_contrast",
                "generate_typography_scale",
                "preview_font_pairing",
                "create_gradient",
                "simulate_color_blindness",
                "export_design_tokens",
                "figma_create_styles",
            ],
            requires_approval=True,  # Art direction requires human approval
        )

    def get_capabilities(self) -> List[str]:
        return [
            "concept_development",
            "color_system_design",
            "typography_system_design",
            "visual_language_definition",
            "motion_principles",
            "direction_documentation",
            "design_token_generation",
        ]

    async def execute(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Execute art direction task."""
        task_type = request.payload.get("task_type", "full_direction")

        if task_type == "full_direction":
            return await self._full_direction(request, context)
        elif task_type == "color_only":
            return await self._color_system_only(request, context)
        elif task_type == "typography_only":
            return await self._typography_system_only(request, context)
        elif task_type == "refine_direction":
            return await self._refine_direction(request, context)
        else:
            return AgentResponse(
                success=False,
                error=f"Unknown task type: {task_type}",
            )

    async def _full_direction(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Create complete artistic direction with multiple options."""
        research_data = context.previous_outputs.get("research", {})
        project_data = request.payload.get("project_context", {})
        brand_personality = project_data.get("design_preferences", {}).get("personality", ["modern", "trustworthy", "clean"])

        # Generate 3 distinct directions
        directions = []
        direction_concepts = [
            {"name": "Clarity & Trust", "metaphor": "Clear sky", "personality": ["professional", "trustworthy", "calm"]},
            {"name": "Bold Innovation", "metaphor": "Breaking dawn", "personality": ["confident", "energetic", "forward"]},
            {"name": "Organic Harmony", "metaphor": "Natural flow", "personality": ["warm", "approachable", "balanced"]},
        ]

        for concept in direction_concepts:
            direction = await self._build_direction(concept, research_data, project_data)
            directions.append(direction)

        # Recommend best direction based on research
        recommendation = self._recommend_direction(directions, research_data, brand_personality)

        result = {
            "directions": directions,
            "recommendation": recommendation,
            "design_tokens_ready": True,
        }

        return AgentResponse(
            success=True,
            result=result,
            tokens_used=self.estimate_tokens(request),
            requires_approval=True,
            approval_payload={
                "phase": "art_direction",
                "data": result,
                "prompt": "Review and approve one artistic direction to proceed to UX/UI design",
            },
        )

    async def _color_system_only(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Generate color system only."""
        direction = request.payload.get("direction", {})
        colors = await self._generate_complete_color_system(direction)
        return AgentResponse(
            success=True,
            result={"colors": colors},
            tokens_used=self.estimate_tokens(request),
        )

    async def _typography_system_only(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Generate typography system only."""
        direction = request.payload.get("direction", {})
        typography = await self._generate_complete_typography_system(direction)
        return AgentResponse(
            success=True,
            result={"typography": typography},
            tokens_used=self.estimate_tokens(request),
        )

    async def _refine_direction(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """Refine an approved direction based on feedback."""
        feedback = request.payload.get("feedback", {})
        current_direction = request.payload.get("current_direction", {})
        # Would apply feedback and regenerate
        refined = current_direction  # Placeholder
        return AgentResponse(
            success=True,
            result={"direction": refined},
            tokens_used=self.estimate_tokens(request),
        )

    async def _build_direction(
        self, concept: Dict, research: Dict, project: Dict
    ) -> Dict[str, Any]:
        """Build a complete artistic direction."""
        colors = await self._generate_complete_color_system(concept)
        typography = await self._generate_complete_typography_system(concept)
        visual_language = self._define_visual_language(concept)
        motion = self._define_motion_principles(concept)
        applications = self._describe_applications(concept, project.get("product_type", "website"))

        return {
            "name": concept["name"],
            "metaphor": concept["metaphor"],
            "personality": concept["personality"],
            "emotional_target": self._get_emotional_target(concept["personality"]),
            "differentiation": self._get_differentiation(concept["name"], research),
            "colors": colors,
            "typography": typography,
            "visual_language": visual_language,
            "motion": motion,
            "applications": applications,
        }

    async def _generate_complete_color_system(self, concept: Dict) -> Dict[str, Any]:
        """Generate complete color system with all scales."""
        # Base hues per concept
        hue_map = {
            "Clarity & Trust": 210,      # Blue
            "Bold Innovation": 280,      # Purple
            "Organic Harmony": 150,      # Green/Teal
        }
        base_hue = hue_map.get(concept["name"], 210)

        # Generate scales (simplified - would use algorithmic generation)
        def gen_scale(hue: int, saturation: int, lightness_base: int) -> Dict[str, str]:
            return {
                "50": f"hsl({hue}, {saturation}%, {lightness_base + 40}%)",
                "100": f"hsl({hue}, {saturation}%, {lightness_base + 35}%)",
                "200": f"hsl({hue}, {saturation}%, {lightness_base + 30}%)",
                "300": f"hsl({hue}, {saturation}%, {lightness_base + 25}%)",
                "400": f"hsl({hue}, {saturation}%, {lightness_base + 15}%)",
                "500": f"hsl({hue}, {saturation}%, {lightness_base}%)",
                "600": f"hsl({hue}, {saturation - 10}%, {lightness_base - 10}%)",
                "700": f"hsl({hue}, {saturation - 5}%, {lightness_base - 20}%)",
                "800": f"hsl({hue}, {saturation}%, {lightness_base - 30}%)",
                "900": f"hsl({hue}, {saturation + 5}%, {lightness_base - 40}%)",
            }

        return {
            "primary": gen_scale(base_hue, 70, 45),
            "secondary": gen_scale((base_hue + 30) % 360, 50, 50),
            "accent": gen_scale((base_hue - 30) % 360, 80, 55),
            "semantic": {
                "success": {"light": "hsl(145, 60%, 42%)", "dark": "hsl(145, 60%, 50%)"},
                "warning": {"light": "hsl(38, 90%, 50%)", "dark": "hsl(38, 90%, 55%)"},
                "error": {"light": "hsl(0, 75%, 50%)", "dark": "hsl(0, 75%, 55%)"},
                "info": {"light": "hsl(200, 80%, 45%)", "dark": "hsl(200, 80%, 55%)"},
            },
            "neutral": gen_scale(220, 10, 50),
            "gradients": [
                {"name": "primary", "stops": ["hsl(210, 70%, 45%)", "hsl(240, 70%, 50%)"]},
                {"name": "accent", "stops": ["hsl(180, 70%, 45%)", "hsl(210, 70%, 50%)"]},
                {"name": "subtle", "stops": ["hsl(210, 20%, 95%)", "hsl(210, 20%, 90%)"]},
            ],
        }

    async def _generate_complete_typography_system(self, concept: Dict) -> Dict[str, Any]:
        """Generate complete typography system."""
        font_map = {
            "Clarity & Trust": {"display": "Inter", "heading": "Inter", "body": "Inter", "mono": "JetBrains Mono"},
            "Bold Innovation": {"display": "Cal Sans", "heading": "Space Grotesk", "body": "Inter", "mono": "JetBrains Mono"},
            "Organic Harmony": {"display": "Fraunces", "heading": "DM Sans", "body": "DM Sans", "mono": "Fira Code"},
        }
        fonts = font_map.get(concept["name"], font_map["Clarity & Trust"])

        return {
            "font_families": fonts,
            "scale": {
                "display_xl": {"size": "clamp(3rem, 8vw, 6rem)", "weight": 700, "line_height": 1.05, "letter_spacing": "-0.03em"},
                "display_lg": {"size": "clamp(2.5rem, 6vw, 4.5rem)", "weight": 700, "line_height": 1.1, "letter_spacing": "-0.02em"},
                "display_md": {"size": "clamp(2rem, 4vw, 3.5rem)", "weight": 600, "line_height": 1.15, "letter_spacing": "-0.01em"},
                "display_sm": {"size": "clamp(1.5rem, 3vw, 2.5rem)", "weight": 600, "line_height": 1.2, "letter_spacing": "0"},
                "heading_1": {"size": "clamp(2rem, 3vw, 3rem)", "weight": 700, "line_height": 1.2},
                "heading_2": {"size": "clamp(1.75rem, 2.5vw, 2.25rem)", "weight": 600, "line_height": 1.25},
                "heading_3": {"size": "clamp(1.5rem, 2vw, 1.875rem)", "weight": 600, "line_height": 1.3},
                "heading_4": {"size": "clamp(1.25rem, 1.5vw, 1.5rem)", "weight": 600, "line_height": 1.35},
                "heading_5": {"size": "1.125rem", "weight": 600, "line_height": 1.4},
                "heading_6": {"size": "1rem", "weight": 600, "line_height": 1.4},
                "body_lg": {"size": "1.125rem", "weight": 400, "line_height": 1.6},
                "body_md": {"size": "1rem", "weight": 400, "line_height": 1.6},
                "body_sm": {"size": "0.875rem", "weight": 400, "line_height": 1.5},
                "body_xs": {"size": "0.75rem", "weight": 400, "line_height": 1.5},
                "label_lg": {"size": "1rem", "weight": 500, "line_height": 1.5},
                "label_md": {"size": "0.875rem", "weight": 500, "line_height": 1.4},
                "label_sm": {"size": "0.75rem", "weight": 500, "line_height": 1.4},
                "caption_md": {"size": "0.75rem", "weight": 400, "line_height": 1.4},
                "caption_sm": {"size": "0.625rem", "weight": 400, "line_height": 1.3},
                "code_md": {"size": "0.875rem", "weight": 400, "line_height": 1.6},
                "code_sm": {"size": "0.75rem", "weight": 400, "line_height": 1.5},
            },
        }

    def _define_visual_language(self, concept: Dict) -> Dict[str, Any]:
        """Define visual language parameters."""
        radius_map = {
            "Clarity & Trust": {"none": "0", "sm": "0.125rem", "md": "0.375rem", "lg": "0.5rem", "xl": "0.75rem", "full": "9999px"},
            "Bold Innovation": {"none": "0", "sm": "0.25rem", "md": "0.5rem", "lg": "0.75rem", "xl": "1rem", "full": "9999px"},
            "Organic Harmony": {"none": "0", "sm": "0.25rem", "md": "0.5rem", "lg": "1rem", "xl": "1.5rem", "full": "9999px"},
        }

        return {
            "border_radius": radius_map.get(concept["name"], radius_map["Clarity & Trust"]),
            "shadows": {
                "1": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
                "2": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
                "3": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
                "4": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)",
                "5": "0 25px 50px -12px rgb(0 0 0 / 0.25)",
            },
            "spacing": {"base": "0.25rem", "scale": [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64]},
            "icon_style": {"type": "outline", "stroke_width": "2", "corner_radius": "round", "padding": "2"},
        }

    def _define_motion_principles(self, concept: Dict) -> Dict[str, Any]:
        """Define motion principles."""
        return {
            "easing": {
                "standard": "cubic-bezier(0.4, 0, 0.2, 1)",
                "expressive": "cubic-bezier(0.34, 1.56, 0.64, 1)",
                "productive": "cubic-bezier(0.4, 0, 0.6, 1)",
            },
            "duration": {"instant": "0ms", "fast": "150ms", "normal": "250ms", "slow": "400ms", "slower": "600ms"},
            "choreography": {"stagger": "50ms", "delay": "100ms"},
        }

    def _describe_applications(self, concept: Dict, product_type: str) -> Dict[str, str]:
        """Describe how direction applies to key screens."""
        return {
            "hero": f"{concept['name']} hero with {concept['metaphor']} imagery",
            "dashboard": f"Clean data visualization with {concept['personality'][0]} tone",
            "mobile": f"Touch-optimized, thumb-friendly {concept['personality'][1]} interface",
        }

    def _get_emotional_target(self, personality: List[str]) -> str:
        """Convert personality to emotional target."""
        return f"Users should feel {', '.join(personality[:-1])} and {personality[-1]}"

    def _get_differentiation(self, name: str, research: Dict) -> str:
        """Explain how this direction differentiates."""
        return f"{name} stands out by emphasizing {name.lower()} unlike competitors who tend toward generic corporate aesthetics"

    def _recommend_direction(self, directions: List[Dict], research: Dict, personality: List[str]) -> Dict[str, Any]:
        """Recommend best direction."""
        # Simple scoring based on personality match
        best_idx = 0
        best_score = 0
        for i, d in enumerate(directions):
            score = sum(1 for p in personality if p in d["personality"])
            if score > best_score:
                best_score = score
                best_idx = i

        return {
            "index": best_idx,
            "rationale": f"Direction '{directions[best_idx]['name']}' best matches brand personality: {', '.join(personality)}",
        }