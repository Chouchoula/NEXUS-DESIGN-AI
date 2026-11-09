"""
NEXUS DESIGN AI - Main API Entry Point for Windows (Fixed)
Autonomous Digital Design Studio Backend
"""

import asyncio
import sys

# Fix for Windows: use SelectorEventLoop instead of ProactorEventLoop
# MUST be set BEFORE any other imports
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Create the event loop with SelectorEventLoop
if sys.platform == "win32":
    import selectors
    loop = asyncio.SelectorEventLoop(selectors.SelectSelector())
    asyncio.set_event_loop(loop)

# Now import and run
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        loop="asyncio",
    )
