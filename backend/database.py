import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# 1. Pull the raw URL from Railway
DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:local_pass@localhost:5432/postgres"
).strip()

# 2. Clean literal quote wrappers if present
if (DATABASE_URL.startswith('"') and DATABASE_URL.endswith('"')) or (DATABASE_URL.startswith("'") and DATABASE_URL.endswith("'")):
    DATABASE_URL = DATABASE_URL[1:-1].strip()

# 3. Create engine letting the connection string handle SSL parameters natively
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