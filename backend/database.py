import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# 1. Fetch from environment, or use a local string fallback for safe development
DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:local_pass@localhost:5432/postgres"
).strip()

# 2. Strip quotes if they somehow snuck back in
if (DATABASE_URL.startswith('"') and DATABASE_URL.endswith('"')) or (DATABASE_URL.startswith("'") and DATABASE_URL.endswith("'")):
    DATABASE_URL = DATABASE_URL[1:-1].strip()

# 3. Secure connection pool configuration arguments
connect_args = {
    "ssl": "require",          # Forces asyncpg to connect over SSL securely to Supabase
    "command_timeout": 60      # Prevents requests from hanging indefinitely
}

# 4. Create the engine with custom arguments and connection timeouts
engine = create_async_engine(
    DATABASE_URL, 
    echo=True, 
    connect_args=connect_args,
    pool_pre_ping=True,        # Checks if connection is alive before handing it to a route
    pool_recycle=1800          # Recycles connections every 30 minutes to prevent stale sockets
)

# 5. Define session maker factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 6. Database dependency injection function
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session