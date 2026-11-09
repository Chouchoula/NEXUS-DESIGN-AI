"""
NEXUS DESIGN AI - Workflow Routes
"""

from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload

from api.database import get_db
from api.models.workflow import Workflow, WorkflowStatus
from api.schemas.workflow import WorkflowCreate, WorkflowUpdate, WorkflowResponse, WorkflowListResponse
from api.workflows import create_design_workflow

router = APIRouter()


@router.post("", response_model=WorkflowResponse, status_code=201)
async def create_workflow(workflow: WorkflowCreate, db: AsyncSession = Depends(get_db)):
    """Create a new workflow."""
    db_workflow = Workflow(**workflow.model_dump())
    db.add(db_workflow)
    await db.commit()
    await db.refresh(db_workflow)
    return db_workflow


@router.get("", response_model=WorkflowListResponse)
async def list_workflows(
    project_id: Optional[UUID] = None,
    status: Optional[WorkflowStatus] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List workflows with filters."""
    query = select(Workflow)

    if project_id:
        query = query.where(Workflow.project_id == project_id)
    if status:
        query = query.where(Workflow.status == status)

    query = query.order_by(desc(Workflow.created_at))

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    # Paginate
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size).options(
        selectinload(Workflow.steps),
    )

    result = await db.execute(query)
    workflows = result.scalars().all()

    return WorkflowListResponse(
        items=workflows,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a workflow by ID."""
    query = select(Workflow).where(Workflow.id == workflow_id).options(
        selectinload(Workflow.steps),
        selectinload(Workflow.tasks),
    )
    result = await db.execute(query)
    workflow = result.scalar_one_or_none()

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return workflow


@router.post("/{workflow_id}/run")
async def run_workflow(
    workflow_id: UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Run a workflow."""
    query = select(Workflow).where(Workflow.id == workflow_id)
    result = await db.execute(query)
    workflow = result.scalar_one_or_none()

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    if workflow.status == WorkflowStatus.RUNNING:
        raise HTTPException(status_code=400, detail="Workflow already running")

    # Update status
    workflow.status = WorkflowStatus.RUNNING
    workflow.started_at = func.now()
    await db.commit()

    # Run workflow in background
    design_workflow = create_design_workflow()
    background_tasks.add_task(
        _execute_workflow,
        design_workflow,
        workflow_id,
    )

    return {"message": "Workflow started", "workflow_id": str(workflow_id)}


async def _execute_workflow(design_workflow, workflow_id: UUID):
    """Execute workflow in background."""
    # This would run the actual workflow
    # Implementation depends on the workflow engine
    pass


@router.post("/{workflow_id}/approve/{phase}")
async def approve_workflow_phase(
    workflow_id: UUID,
    phase: str,
    approved: bool = True,
    feedback: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Approve or reject a workflow phase."""
    query = select(Workflow).where(Workflow.id == workflow_id)
    result = await db.execute(query)
    workflow = result.scalar_one_or_none()

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # Update step status
    for step in workflow.steps:
        if step.name.lower().replace(" ", "_") == phase:
            step.approved = approved
            step.approval_notes = feedback
            step.status = "completed" if approved else "failed"
            step.completed_at = func.now()
            break

    await db.commit()
    return {"message": f"Phase {phase} {'approved' if approved else 'rejected'}"}


@router.patch("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: UUID, workflow_update: WorkflowUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a workflow."""
    query = select(Workflow).where(Workflow.id == workflow_id)
    result = await db.execute(query)
    workflow = result.scalar_one_or_none()

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    update_data = workflow_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(workflow, field, value)

    await db.commit()
    await db.refresh(workflow)
    return workflow