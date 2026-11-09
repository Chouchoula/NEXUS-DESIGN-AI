"""
NEXUS DESIGN AI - Design System Models
"""

import enum
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    String, Text, DateTime, Enum, ForeignKey, JSON, Index, func, Integer
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from api.database import Base


class DesignSystem(Base):
    """Design system for a project."""

    __tablename__ = "design_systems"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    version: Mapped[str] = mapped_column(String(50), default="1.0.0")

    # Global settings
    css_variables: Mapped[Optional[Dict[str, str]]] = mapped_column(JSON, nullable=True)
    tailwind_config: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="design_system", lazy="selectin")
    color_tokens: Mapped[List["ColorToken"]] = relationship("ColorToken", back_populates="design_system", lazy="selectin", cascade="all, delete-orphan")
    typography_tokens: Mapped[List["TypographyToken"]] = relationship("TypographyToken", back_populates="design_system", lazy="selectin", cascade="all, delete-orphan")
    spacing_tokens: Mapped[List["SpacingToken"]] = relationship("SpacingToken", back_populates="design_system", lazy="selectin", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<DesignSystem(id={self.id}, name='{self.name}')>"


class ColorToken(Base):
    """Color design token."""

    __tablename__ = "color_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    design_system_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("design_systems.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g., "primary-500"
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # primary, secondary, accent, semantic, neutral
    value_light: Mapped[str] = mapped_column(String(20), nullable=False)  # hex for light mode
    value_dark: Mapped[str] = mapped_column(String(20), nullable=False)  # hex for dark mode
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    design_system: Mapped["DesignSystem"] = relationship("DesignSystem", back_populates="color_tokens", lazy="selectin")

    # Indexes
    __table_args__ = (
        Index("ix_color_tokens_design_system_id", "design_system_id"),
        Index("ix_color_tokens_category", "category"),
    )

    def __repr__(self) -> str:
        return f"<ColorToken(name='{self.name}', light={self.value_light}, dark={self.value_dark})>"


class TypographyToken(Base):
    """Typography design token."""

    __tablename__ = "typography_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    design_system_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("design_systems.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g., "heading-1", "body-md"
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # heading, body, label, caption
    font_family: Mapped[str] = mapped_column(String(100), nullable=False)
    font_weight: Mapped[int] = mapped_column(Integer, default=400)
    font_size: Mapped[str] = mapped_column(String(20), nullable=False)  # rem value
    line_height: Mapped[str] = mapped_column(String(20), nullable=False)
    letter_spacing: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    text_transform: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # uppercase, lowercase, etc.
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    design_system: Mapped["DesignSystem"] = relationship("DesignSystem", back_populates="typography_tokens", lazy="selectin")

    # Indexes
    __table_args__ = (
        Index("ix_typography_tokens_design_system_id", "design_system_id"),
        Index("ix_typography_tokens_category", "category"),
    )

    def __repr__(self) -> str:
        return f"<TypographyToken(name='{self.name}', size={self.font_size})>"


class SpacingToken(Base):
    """Spacing design token."""

    __tablename__ = "spacing_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    design_system_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("design_systems.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., "space-4", "space-lg"
    value: Mapped[str] = mapped_column(String(20), nullable=False)  # rem value
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    design_system: Mapped["DesignSystem"] = relationship("DesignSystem", back_populates="spacing_tokens", lazy="selectin")

    # Indexes
    __table_args__ = (
        Index("ix_spacing_tokens_design_system_id", "design_system_id"),
    )

    def __repr__(self) -> str:
        return f"<SpacingToken(name='{self.name}', value={self.value})>"