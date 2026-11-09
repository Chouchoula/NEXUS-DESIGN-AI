import asyncio
import sys
import os
import tempfile

# Fix for Windows: use SelectorEventLoop instead of ProactorEventLoop
# MUST be set BEFORE any other imports
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

print(f"Event loop policy: {asyncio.get_event_loop_policy().__class__.__name__}")

# Test with SQLite
db_path = os.path.join(tempfile.gettempdir(), 'test_nexus.db')
print(f"Test DB path: {db_path}")

from sqlalchemy.ext.asyncio import create_async_engine
engine = create_async_engine(f'sqlite+aiosqlite:///{db_path}', echo=True)

async def test():
    async with engine.begin() as conn:
        from sqlalchemy import text
        result = await conn.execute(text('SELECT 1'))
        print(f"SQLite test result: {result.scalar()}")
    await engine.dispose()
    print("SQLite connection test passed!")

asyncio.run(test())
