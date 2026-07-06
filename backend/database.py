import os
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# 1. Break the credentials down directly into isolated strings
# Note: Use your raw password here without any percent-encoding tricks!
db_url = URL.create(
    drivername="postgresql+asyncpg",
    username="postgres",
    password="paul-dev@0069", 
    host="db.uferjqmwphjgifdaanmp.supabase.co",
    port=5432,
    database="postgres",
    query={"sslmode": "require"}
)

# 2. Spin up the engine using the clean structural object
engine = create_async_engine(
    db_url, 
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