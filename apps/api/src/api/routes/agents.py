"""
NEXUS DESIGN AI - Agent Routes
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload

from api.database import get_db
from api.models.agent_task import AgentTask, TaskStatus, AgentType
from api.schemas.agent_task import AgentTaskCreate, AgentTaskUpdate, AgentTaskResponse

router = APIRouter()


@router.post("/tasks", response_model=AgentTaskResponse, status_code=201)
async def create_agent_task(task: AgentTaskCreate, db: AsyncSession = Depends(get_db)):
    """Create a new agent task."""
    db_task = AgentTask(**task.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


@router.get("/tasks", response_model=List[AgentTaskResponse])
async def list_agent_tasks(
    project_id: Optional[UUID] = None,
    agent_type: Optional[AgentType] = None,
    status: Optional[TaskStatus] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List agent tasks with filters."""
    query = select(AgentTask)

    if project_id:
        query = query.where(AgentTask.project_id == project_id)
    if agent_type:
        query = query.where(AgentTask.agent_type == agent_type)
    if status:
        query = query.where(AgentTask.status == status)

    query = query.order_by(desc(AgentTask.created_at))

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/tasks/{task_id}", response_model=AgentTaskResponse)
async def get_agent_task(task_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get an agent task by ID."""
    query = select(AgentTask).where(AgentTask.id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.patch("/tasks/{task_id}", response_model=AgentTaskResponse)
async def update_agent_task(
    task_id: UUID, task_update: AgentTaskUpdate, db: AsyncSession = Depends(get_db)
):
    """Update an agent task."""
    query = select(AgentTask).where(AgentTask.id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)
    return task


@router.get("/status", response_model=List[dict])
async def get_agents_status():
    """Get status of all agents."""
    # This would query the actual agent instances
    # For now, return static status
    return [
        {"agent_type": "orchestrator", "status": "idle", "tasks_completed": 0},
        {"agent_type": "research", "status": "idle", "tasks_completed": 0},
        {"agent_type": "art_director", "status": "idle", "tasks_completed": 0},
        {"agent_type": "ux_designer", "status": "idle", "tasks_completed": 0},
        {"agent_type": "ui_designer", "status": "idle", "tasks_completed": 0},
        {"agent_type": "frontend_engineer", "status": "idle", "tasks_completed": 0},
        {"agent_type": "visual_qa", "status": "idle", "tasks_completed": 0},
    ]