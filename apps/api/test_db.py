"""
Test database connection with event loop fix
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

# Use the loop variable we created
print(f"Event loop: {loop.__class__.__name__}")

# Now test database
from api.config import settings
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)

async def test_connection():
    async with engine.begin() as conn:
        from sqlalchemy import text
        result = await conn.execute(text("SELECT 1"))
        print(f"Connection test result: {result.scalar()}")
    await engine.dispose()
    print("Connection test passed!")

loop.run_until_complete(test_connection())
