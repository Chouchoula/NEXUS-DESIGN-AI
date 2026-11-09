"""
Test script to verify event loop policy fix
"""
import asyncio
import sys

# Fix for Windows: use SelectorEventLoop instead of ProactorEventLoop
# MUST be set BEFORE any other imports
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Verify the policy is set correctly
print(f"Event loop policy: {asyncio.get_event_loop_policy().__class__.__name__}")

# Now test creating an async engine
from sqlalchemy.ext.asyncio import create_async_engine
from api.config import settings

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

asyncio.run(test_connection())