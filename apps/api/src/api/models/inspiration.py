"""
NEXUS DESIGN AI - Inspiration Models
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


class InspirationSource(str, enum.Enum):
    """Sources of inspiration."""
    FIGMA_COMMUNITY = "figma_community"
    PINTEREST = "pinterest"
    DRIBBBLE = "dribbble"
    BEHANCE = "behance"
    AWWWARDS = "awwwards"
    MOBBIN = "mobbin"
    GODLY = "godly"
    LAND_BOOK = "land_book"
    SITE_INSPIRE = "site_inspire"
    REFERO = "refero"
    FRAMER = "framer"
    PENPOT = "penpot"
    UNSPLASH = "unsplash"
    PEXELS = "pexels"
    ICONIFY = "iconify"
    GOOGLE_FONTS = "google_fonts"
    LOTTIEFILES = "lottiefiles"
    CUSTOM = "custom"


class Inspiration(Base):
    """Visual inspiration and reference entity."""

    __tablename__ = "inspirations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[InspirationSource] = mapped_column(Enum(InspirationSource), nullable=False)
    source_url: Mapped[str] = mapped_column(String(500), nullable=False)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    local_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Categorization
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # fintech, health, ecommerce, etc.
    style_tags: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)  # minimal, bold, dark, glassmorphism, etc.
    product_types: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)  # website, mobile, dashboard, etc.
    platforms: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)  # web, ios, android, desktop

    # Extracted design attributes
    color_palette: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    typography: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    components: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    layout_patterns: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    animations: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)

    # Quality metrics
    relevance_score: Mapped[Optional[float]] = mapped_column(nullable=True)  # 0-1
    aesthetic_score: Mapped[Optional[float]] = mapped_column(nullable=True)  # 0-1
    usability_score: Mapped[Optional[float]] = mapped_column(nullable=True)  # 0-1

    # License and usage
    license: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    commercial_use: Mapped[Optional[bool]] = mapped_column(nullable=True)
    attribution_required: Mapped[bool] = mapped_column(default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Indexes
    __table_args__ = (
        Index("ix_inspirations_project_id", "project_id"),
        Index("ix_inspirations_source", "source"),
        Index("ix_inspirations_category", "category"),
        Index("ix_inspirations_style_tags", "style_tags", postgresql_using="gin"),
    )

    def __repr__(self) -> str:
        return f"<Inspiration(id={self.id}, title='{self.title}', source={self.source})>"