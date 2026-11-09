"""
NEXUS DESIGN AI - Figma Integration Routes
"""

from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from api.config import settings

router = APIRouter()


class FigmaFile(BaseModel):
    """Figma file representation."""
    key: str
    name: str
    thumbnail_url: Optional[str] = None
    last_modified: str
    version: str
    branches: List[dict] = []


class FigmaComponent(BaseModel):
    """Figma component representation."""
    key: str
    name: str
    description: Optional[str] = None
    component_set_id: Optional[str] = None
    variants: List[dict] = []


class FigmaStyle(BaseModel):
    """Figma style representation."""
    key: str
    name: str
    style_type: str  # FILL, TEXT, EFFECT, GRID
    value: dict


@router.get("/files/{file_key}", response_model=FigmaFile)
async def get_figma_file(file_key: str):
    """Get Figma file metadata."""
    if not settings.FIGMA_ACCESS_TOKEN:
        raise HTTPException(status_code=400, detail="Figma access token not configured")

    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.figma.com/v1/files/{file_key}",
            headers={"X-Figma-Token": settings.FIGMA_ACCESS_TOKEN},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch Figma file")
        return response.json()


@router.get("/files/{file_key}/nodes")
async def get_figma_nodes(file_key: str, ids: str = Query(...)):
    """Get specific nodes from Figma file."""
    if not settings.FIGMA_ACCESS_TOKEN:
        raise HTTPException(status_code=400, detail="Figma access token not configured")

    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.figma.com/v1/files/{file_key}/nodes",
            params={"ids": ids},
            headers={"X-Figma-Token": settings.FIGMA_ACCESS_TOKEN},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch Figma nodes")
        return response.json()


@router.get("/files/{file_key}/components", response_model=List[FigmaComponent])
async def get_figma_components(file_key: str):
    """Get components from Figma file."""
    if not settings.FIGMA_ACCESS_TOKEN:
        raise HTTPException(status_code=400, detail="Figma access token not configured")

    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.figma.com/v1/files/{file_key}/components",
            headers={"X-Figma-Token": settings.FIGMA_ACCESS_TOKEN},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch Figma components")
        data = response.json()
        return data.get("meta", {}).get("components", {}).values()


@router.get("/files/{file_key}/styles", response_model=List[FigmaStyle])
async def get_figma_styles(file_key: str):
    """Get styles from Figma file."""
    if not settings.FIGMA_ACCESS_TOKEN:
        raise HTTPException(status_code=400, detail="Figma access token not configured")

    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.figma.com/v1/files/{file_key}/styles",
            headers={"X-Figma-Token": settings.FIGMA_ACCESS_TOKEN},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch Figma styles")
        data = response.json()
        return data.get("meta", {}).get("styles", {}).values()


@router.get("/files/{file_key}/images")
async def get_figma_images(file_key: str, ids: str = Query(...), format: str = "png", scale: float = 2.0):
    """Export images from Figma file."""
    if not settings.FIGMA_ACCESS_TOKEN:
        raise HTTPException(status_code=400, detail="Figma access token not configured")

    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.figma.com/v1/images/{file_key}",
            params={"ids": ids, "format": format, "scale": scale},
            headers={"X-Figma-Token": settings.FIGMA_ACCESS_TOKEN},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to export Figma images")
        return response.json()


@router.post("/files/{file_key}/comments")
async def post_figma_comment(file_key: str, message: str, client_meta: Optional[dict] = None):
    """Post comment to Figma file."""
    if not settings.FIGMA_ACCESS_TOKEN:
        raise HTTPException(status_code=400, detail="Figma access token not configured")

    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.figma.com/v1/files/{file_key}/comments",
            json={"message": message, "client_meta": client_meta or {}},
            headers={"X-Figma-Token": settings.FIGMA_ACCESS_TOKEN},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to post Figma comment")
        return response.json()


@router.get("/team/{team_id}/projects")
async def get_team_projects(team_id: str):
    """Get team projects."""
    if not settings.FIGMA_ACCESS_TOKEN:
        raise HTTPException(status_code=400, detail="Figma access token not configured")

    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.figma.com/v1/teams/{team_id}/projects",
            headers={"X-Figma-Token": settings.FIGMA_ACCESS_TOKEN},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch team projects")
        return response.json()


@router.get("/me")
async def get_current_user():
    """Get current Figma user."""
    if not settings.FIGMA_ACCESS_TOKEN:
        raise HTTPException(status_code=400, detail="Figma access token not configured")

    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.figma.com/v1/me",
            headers={"X-Figma-Token": settings.FIGMA_ACCESS_TOKEN},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch user")
        return response.json()