import os
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker


raw_url = os.environ.get("DATABASE_URL", "").strip()

# 2. Strip out hidden literal outer quotation marks if Render accidentally wrapped the value
if (raw_url.startswith('"') and raw_url.endswith('"')) or (raw_url.startswith("'") and raw_url.endswith("'")):
    raw_url = raw_url[1:-1].strip()

# 3. Handle accidental URL double-encoding of special characters (like %40 converting to %2540)
if "%2540" in raw_url:
    raw_url = raw_url.replace("%2540", "%40")

DATABASE_URL = raw_url

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_= AsyncSession,
    expire_on_commit= False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


import os
from sqlalchemy.ext.asyncio import create_async_engine



