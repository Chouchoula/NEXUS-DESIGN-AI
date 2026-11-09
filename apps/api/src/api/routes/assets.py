"""
NEXUS DESIGN AI - Asset Routes
"""

from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload

from api.database import get_db
from api.models.asset import Asset, AssetCategory, AssetStatus
from api.schemas.asset import AssetCreate, AssetUpdate, AssetResponse, AssetListResponse

router = APIRouter()


@router.post("", response_model=AssetResponse, status_code=201)
async def create_asset(asset: AssetCreate, db: AsyncSession = Depends(get_db)):
    """Create a new asset."""
    db_asset = Asset(**asset.model_dump())
    db.add(db_asset)
    await db.commit()
    await db.refresh(db_asset)
    return db_asset


@router.post("/upload", response_model=AssetResponse, status_code=201)
async def upload_asset(
    file: UploadFile = File(...),
    project_id: Optional[UUID] = Form(None),
    name: str = Form(...),
    category: AssetCategory = Form(...),
    source: str = Form(...),
    source_url: Optional[str] = Form(None),
    license: Optional[str] = Form(None),
    commercial_use: Optional[bool] = Form(None),
    attribution_required: bool = Form(False),
    tags: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
):
    """Upload an asset file."""
    # In real implementation, save file to storage (S3, local, etc.)
    # For now, create asset record
    db_asset = Asset(
        project_id=project_id,
        name=name,
        category=category,
        source=source,
        source_url=source_url,
        license=license,
        commercial_use=commercial_use,
        attribution_required=attribution_required,
        tags=tags.split(",") if tags else None,
        file_format=file.content_type,
        status=AssetStatus.PENDING_REVIEW,
    )
    db.add(db_asset)
    await db.commit()
    await db.refresh(db_asset)
    return db_asset


@router.get("", response_model=AssetListResponse)
async def list_assets(
    project_id: Optional[UUID] = None,
    category: Optional[AssetCategory] = None,
    status: Optional[AssetStatus] = None,
    source: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List assets with filters."""
    query = select(Asset)

    if project_id:
        query = query.where(Asset.project_id == project_id)
    if category:
        query = query.where(Asset.category == category)
    if status:
        query = query.where(Asset.status == status)
    if source:
        query = query.where(Asset.source == source)

    query = query.order_by(desc(Asset.created_at))

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    # Paginate
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    assets = result.scalars().all()

    return AssetListResponse(
        items=assets,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(asset_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get an asset by ID."""
    query = select(Asset).where(Asset.id == asset_id)
    result = await db.execute(query)
    asset = result.scalar_one_or_none()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    return asset


@router.patch("/{asset_id}", response_model=AssetResponse)
async def update_asset(
    asset_id: UUID, asset_update: AssetUpdate, db: AsyncSession = Depends(get_db)
):
    """Update an asset."""
    query = select(Asset).where(Asset.id == asset_id)
    result = await db.execute(query)
    asset = result.scalar_one_or_none()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    update_data = asset_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(asset, field, value)

    await db.commit()
    await db.refresh(asset)
    return asset


@router.delete("/{asset_id}", status_code=204)
async def delete_asset(asset_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete an asset."""
    query = select(Asset).where(Asset.id == asset_id)
    result = await db.execute(query)
    asset = result.scalar_one_or_none()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    await db.delete(asset)
    await db.commit()


@router.get("/categories/list")
async def list_categories():
    """List all asset categories."""
    return [{"value": c.value, "label": c.value.replace("_", " ").title()} for c in AssetCategory]


@router.get("/sources/list")
async def list_sources():
    """List known asset sources."""
    return [
        "figma_community",
        "pinterest",
        "dribbble",
        "behance",
        "awwwards",
        "mobbin",
        "godly",
        "land_book",
        "site_inspire",
        "refero",
        "framer",
        "penpot",
        "unsplash",
        "pexels",
        "pixabay",
        "iconify",
        "google_fonts",
        "lottiefiles",
        "custom",
    ]