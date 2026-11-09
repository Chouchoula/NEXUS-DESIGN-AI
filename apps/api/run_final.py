"""
NEXUS DESIGN AI - Main API Entry Point for Windows (Fixed)
Autonomous Digital Design Studio Backend
"""

import sys
import os

# Set the environment variable BEFORE importing anything else
os.environ["UVICORN_LOOP"] = "asyncio"

# Fix for Windows: use SelectorEventLoop instead of ProactorEventLoop
# MUST be set BEFORE any other imports
if sys.platform == "win32":
    import asyncio
    import selectors
    
    # Create and set the selector event loop
    loop = asyncio.SelectorEventLoop(selectors.SelectSelector())
    asyncio.set_event_loop(loop)

# Now import and run uvicorn
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )
