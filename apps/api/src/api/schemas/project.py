"""
NEXUS DESIGN AI - Project Schemas
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

from api.models.project import ProductType, ProjectStatus


class ProjectBase(BaseModel):
    """Base project schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    product_type: ProductType
    target_audience: Optional[str] = None
    business_goals: Optional[List[str]] = None
    technical_constraints: Optional[Dict[str, Any]] = None
    design_preferences: Optional[Dict[str, Any]] = None
    repo_url: Optional[str] = None
    repo_branch: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    product_type: Optional[ProductType] = None
    status: Optional[ProjectStatus] = None
    target_audience: Optional[str] = None
    business_goals: Optional[List[str]] = None
    technical_constraints: Optional[Dict[str, Any]] = None
    design_preferences: Optional[Dict[str, Any]] = None
    repo_url: Optional[str] = None
    repo_branch: Optional[str] = None


class ProjectResponse(ProjectBase):
    """Schema for project response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    # Counts
    assets_count: int = 0
    tasks_count: int = 0
    workflows_count: int = 0


class ProjectListResponse(BaseModel):
    """Schema for paginated project list."""
    items: List[ProjectResponse]
    total: int
    page: int
    page_size: int
    total_pages: int