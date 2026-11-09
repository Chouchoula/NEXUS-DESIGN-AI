"""
NEXUS DESIGN AI - Asset Schemas
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

from api.models.asset import AssetCategory, AssetStatus


class AssetBase(BaseModel):
    """Base asset schema."""
    name: str = Field(..., min_length=1, max_length=255)
    category: AssetCategory
    source: str = Field(..., min_length=1, max_length=100)
    source_url: Optional[str] = None
    asset_url: Optional[str] = None
    local_path: Optional[str] = None
    license: Optional[str] = None
    commercial_use: Optional[bool] = None
    attribution_required: bool = False
    tags: Optional[List[str]] = None
    dominant_colors: Optional[List[str]] = None
    dimensions: Optional[Dict[str, int]] = None
    file_format: Optional[str] = None
    file_size: Optional[int] = None
    style: Optional[str] = None


class AssetCreate(AssetBase):
    """Schema for creating an asset."""
    project_id: Optional[UUID] = None


class AssetUpdate(BaseModel):
    """Schema for updating an asset."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[AssetCategory] = None
    status: Optional[AssetStatus] = None
    source_url: Optional[str] = None
    asset_url: Optional[str] = None
    local_path: Optional[str] = None
    license: Optional[str] = None
    commercial_use: Optional[bool] = None
    attribution_required: Optional[bool] = None
    tags: Optional[List[str]] = None
    dominant_colors: Optional[List[str]] = None
    style: Optional[str] = None


class AssetResponse(AssetBase):
    """Schema for asset response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: Optional[UUID] = None
    status: AssetStatus
    used_in_projects: Optional[List[UUID]] = None
    download_count: int = 0
    created_at: datetime
    updated_at: datetime


class AssetListResponse(BaseModel):
    """Schema for paginated asset list."""
    items: List[AssetResponse]
    total: int
    page: int
    page_size: int
    total_pages: int