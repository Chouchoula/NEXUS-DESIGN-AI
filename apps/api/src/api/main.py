"""
NEXUS DESIGN AI - Main API Entry Point
Autonomous Digital Design Studio Backend
"""

import sys

# Fix for Windows: use SelectorEventLoop instead of ProactorEventLoop
# MUST be set BEFORE any other imports, especially database
if sys.platform == "win32":
    import asyncio
    import selectors
    selector = selectors.SelectSelector()
    loop = asyncio.SelectorEventLoop(selector)
    asyncio.set_event_loop(loop)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Import database FIRST to set the event loop policy before any other asyncio operations
from api import database  # noqa: F401

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.config import settings
from api.database import init_db, close_db
from api.routes import projects, agents, workflows, assets, figma, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


app = FastAPI(
    title="NEXUS DESIGN AI",
    description="Autonomous Digital Design Studio API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(workflows.router, prefix="/api/v1/workflows", tags=["workflows"])
app.include_router(assets.router, prefix="/api/v1/assets", tags=["assets"])
app.include_router(figma.router, prefix="/api/v1/figma", tags=["figma"])


@app.get("/")
async def root():
    return {
        "name": "NEXUS DESIGN AI",
        "version": "1.0.0",
        "description": "Autonomous Digital Design Studio",
        "status": "operational",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
