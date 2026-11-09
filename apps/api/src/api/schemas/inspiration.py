"""
NEXUS DESIGN AI - Inspiration Schemas
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

from api.models.inspiration import InspirationSource


class InspirationBase(BaseModel):
    """Base inspiration schema."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    source: InspirationSource
    source_url: str = Field(..., min_length=1, max_length=500)
    thumbnail_url: Optional[str] = None
    local_path: Optional[str] = None
    category: Optional[str] = None
    style_tags: Optional[List[str]] = None
    product_types: Optional[List[str]] = None
    platforms: Optional[List[str]] = None
    color_palette: Optional[List[str]] = None
    typography: Optional[Dict[str, Any]] = None
    components: Optional[List[str]] = None
    layout_patterns: Optional[List[str]] = None
    animations: Optional[List[str]] = None
    relevance_score: Optional[float] = Field(None, ge=0, le=1)
    aesthetic_score: Optional[float] = Field(None, ge=0, le=1)
    usability_score: Optional[float] = Field(None, ge=0, le=1)
    license: Optional[str] = None
    commercial_use: Optional[bool] = None
    attribution_required: bool = False


class InspirationCreate(InspirationBase):
    """Schema for creating an inspiration."""
    project_id: Optional[UUID] = None


class InspirationUpdate(BaseModel):
    """Schema for updating an inspiration."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    style_tags: Optional[List[str]] = None
    product_types: Optional[List[str]] = None
    platforms: Optional[List[str]] = None
    relevance_score: Optional[float] = Field(None, ge=0, le=1)
    aesthetic_score: Optional[float] = Field(None, ge=0, le=1)
    usability_score: Optional[float] = Field(None, ge=0, le=1)


class InspirationResponse(InspirationBase):
    """Schema for inspiration response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime


class InspirationListResponse(BaseModel):
    """Schema for paginated inspiration list."""
    items: List[InspirationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int