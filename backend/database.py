import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# 1. Fetch the dynamic variable provided natively by Railway
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

# 2. Fix the driver protocol prefix for SQLAlchemy Asyncio if needed
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# 3. Spin up the clean engine over the internal cloud network
engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session