"""
NEXUS DESIGN AI - Design System Schemas
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID


class DesignSystemBase(BaseModel):
    """Base design system schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    version: str = "1.0.0"
    css_variables: Optional[Dict[str, str]] = None
    tailwind_config: Optional[Dict[str, Any]] = None


class DesignSystemCreate(DesignSystemBase):
    """Schema for creating a design system."""
    project_id: UUID


class DesignSystemUpdate(BaseModel):
    """Schema for updating a design system."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    version: Optional[str] = None
    css_variables: Optional[Dict[str, str]] = None
    tailwind_config: Optional[Dict[str, Any]] = None


class DesignSystemResponse(DesignSystemBase):
    """Schema for design system response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime


# Color Tokens
class ColorTokenBase(BaseModel):
    """Base color token schema."""
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=50)
    value_light: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    value_dark: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    description: Optional[str] = None
    order: int = 0


class ColorTokenCreate(ColorTokenBase):
    """Schema for creating a color token."""
    design_system_id: UUID


class ColorTokenUpdate(BaseModel):
    """Schema for updating a color token."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    value_light: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    value_dark: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    description: Optional[str] = None
    order: Optional[int] = None


class ColorTokenResponse(ColorTokenBase):
    """Schema for color token response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    design_system_id: UUID


# Typography Tokens
class TypographyTokenBase(BaseModel):
    """Base typography token schema."""
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=50)
    font_family: str = Field(..., min_length=1, max_length=100)
    font_weight: int = Field(..., ge=100, le=900)
    font_size: str = Field(..., min_length=1, max_length=20)
    line_height: str = Field(..., min_length=1, max_length=20)
    letter_spacing: Optional[str] = Field(None, max_length=20)
    text_transform: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    order: int = 0


class TypographyTokenCreate(TypographyTokenBase):
    """Schema for creating a typography token."""
    design_system_id: UUID


class TypographyTokenUpdate(BaseModel):
    """Schema for updating a typography token."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    font_family: Optional[str] = Field(None, min_length=1, max_length=100)
    font_weight: Optional[int] = Field(None, ge=100, le=900)
    font_size: Optional[str] = Field(None, min_length=1, max_length=20)
    line_height: Optional[str] = Field(None, min_length=1, max_length=20)
    letter_spacing: Optional[str] = Field(None, max_length=20)
    text_transform: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    order: Optional[int] = None


class TypographyTokenResponse(TypographyTokenBase):
    """Schema for typography token response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    design_system_id: UUID


# Spacing Tokens
class SpacingTokenBase(BaseModel):
    """Base spacing token schema."""
    name: str = Field(..., min_length=1, max_length=50)
    value: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    order: int = 0


class SpacingTokenCreate(SpacingTokenBase):
    """Schema for creating a spacing token."""
    design_system_id: UUID


class SpacingTokenUpdate(BaseModel):
    """Schema for updating a spacing token."""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    value: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    order: Optional[int] = None


class SpacingTokenResponse(SpacingTokenBase):
    """Schema for spacing token response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    design_system_id: UUID