"""
NEXUS DESIGN AI - Asset Models
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


class AssetCategory(str, enum.Enum):
    """Categories of design assets."""
    ICON = "icon"
    ILLUSTRATION = "illustration"
    BACKGROUND = "background"
    TEXTURE = "texture"
    PHOTOGRAPH = "photograph"
    LOGO = "logo"
    ANIMATION = "animation"
    FONT = "font"
    COLOR_PALETTE = "color_palette"
    UI_COMPONENT = "ui_component"
    TEMPLATE = "template"
    REFERENCE = "reference"


class AssetStatus(str, enum.Enum):
    """Asset processing status."""
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class Asset(Base):
    """Design asset entity."""

    __tablename__ = "assets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[AssetCategory] = mapped_column(Enum(AssetCategory), nullable=False)
    status: Mapped[AssetStatus] = mapped_column(
        Enum(AssetStatus), default=AssetStatus.PENDING_REVIEW, nullable=False
    )

    # Source information
    source: Mapped[str] = mapped_column(String(100), nullable=False)  # unsplash, pexels, figma, etc.
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    asset_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    local_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # License and usage
    license: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    commercial_use: Mapped[Optional[bool]] = mapped_column(nullable=True)
    attribution_required: Mapped[bool] = mapped_column(default=False)

    # Metadata
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    dominant_colors: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    dimensions: Mapped[Optional[Dict[str, int]]] = mapped_column(JSON, nullable=True)  # width, height
    file_format: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(nullable=True)  # bytes
    style: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Usage tracking
    used_in_projects: Mapped[Optional[List[uuid.UUID]]] = mapped_column(JSON, nullable=True)
    download_count: Mapped[int] = mapped_column(default=0)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    project: Mapped[Optional["Project"]] = relationship("Project", back_populates="assets", lazy="selectin")

    # Indexes
    __table_args__ = (
        Index("ix_assets_category", "category"),
        Index("ix_assets_status", "status"),
        Index("ix_assets_source", "source"),
        Index("ix_assets_project_id", "project_id"),
        Index("ix_assets_tags", "tags", postgresql_using="gin"),
    )

    def __repr__(self) -> str:
        return f"<Asset(id={self.id}, name='{self.name}', category={self.category})>"