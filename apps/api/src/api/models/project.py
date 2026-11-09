"""
NEXUS DESIGN AI - Project Models
"""

import enum
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    String, Text, DateTime, Enum, ForeignKey, JSON, Index, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from api.database import Base


class ProductType(str, enum.Enum):
    """Types of products NEXUS can design."""
    WEBSITE = "website"
    MOBILE_APP = "mobile_app"
    DASHBOARD = "dashboard"
    SAAS = "saas"
    DESKTOP_APP = "desktop_app"
    BRAND_IDENTITY = "brand_identity"


class ProjectStatus(str, enum.Enum):
    """Project lifecycle status."""
    DRAFT = "draft"
    RESEARCH = "research"
    ART_DIRECTION = "art_direction"
    UX_DESIGN = "ux_design"
    UI_DESIGN = "ui_design"
    DEVELOPMENT = "development"
    QA = "qa"
    REVIEW = "review"
    DELIVERED = "delivered"
    ARCHIVED = "archived"


class Project(Base):
    """Main project entity."""

    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    product_type: Mapped[ProductType] = mapped_column(
        Enum(ProductType), nullable=False
    )
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus), default=ProjectStatus.DRAFT, nullable=False
    )

    # Target audience and context
    target_audience: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    business_goals: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    technical_constraints: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    design_preferences: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Repository info
    repo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    repo_branch: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    assets: Mapped[List["Asset"]] = relationship("Asset", back_populates="project", lazy="selectin")
    tasks: Mapped[List["AgentTask"]] = relationship("AgentTask", back_populates="project", lazy="selectin")
    workflows: Mapped[List["Workflow"]] = relationship("Workflow", back_populates="project", lazy="selectin")
    design_system: Mapped[Optional["DesignSystem"]] = relationship("DesignSystem", back_populates="project", uselist=False, lazy="selectin")

    # Indexes
    __table_args__ = (
        Index("ix_projects_status", "status"),
        Index("ix_projects_product_type", "product_type"),
        Index("ix_projects_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name='{self.name}', status={self.status})>"