import os
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker


DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:local_pass@localhost:5432/postgres"
).strip()


if not DATABASE_URL:
    raise ValueError("CRITICAL ERROR: DATABASE_URL environment variable is completely empty or not found!")

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



