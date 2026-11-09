"""
NEXUS DESIGN AI - Main API Entry Point for Windows (Fixed)
Autonomous Digital Design Studio Backend
"""

import asyncio
import sys
import selectors

# Create a custom loop factory that uses SelectorEventLoop
def create_selector_loop():
    """Create a SelectorEventLoop for Windows."""
    return asyncio.SelectorEventLoop(selectors.SelectSelector())

async def main():
    # Set the event loop policy
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Create our own event loop
    loop = create_selector_loop()
    asyncio.set_event_loop(loop)
    
    import uvicorn
    
    config = uvicorn.Config(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    # Use custom loop factory
    asyncio.run(main(), loop_factory=create_selector_loop)
