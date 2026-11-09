"""
Site customization for Windows event loop fix.
This runs BEFORE any other imports when Python starts.
"""

import sys

if sys.platform == "win32":
    import asyncio
    import selectors
    
    # Create and set the selector event loop as the default
    selector = selectors.SelectSelector()
    loop = asyncio.SelectorEventLoop(selector)
    asyncio.set_event_loop(loop)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
