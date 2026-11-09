"""
NEXUS DESIGN AI - Main API Entry Point for Windows (Fixed)
Autonomous Digital Design Studio Backend
"""

import asyncio
import sys
import selectors
import os

# Must be set BEFORE any imports
os.environ["UVICORN_LOOP"] = "asyncio"

# Create the selector event loop FIRST
if sys.platform == "win32":
    selector = selectors.SelectSelector()
    loop = asyncio.SelectorEventLoop(selector)
    asyncio.set_event_loop(loop)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Import the app AFTER setting the loop
from api.main import app

# Pre-initialize database in the main process
async def init_database():
    from api.database import init_db
    await init_db()

if __name__ == "__main__":
    # Pre-initialize database
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_database())
    
    # Now run uvicorn with the app object - NO WORKERS
    import uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False,
        workers=None,  # No workers - single process
        loop="asyncio",
    )
