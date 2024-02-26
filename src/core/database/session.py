import sys
from sqlalchemy.pool import NullPool, QueuePool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
import asyncio
import sys

from src.core.config import settings

DB_POOL_SIZE = 83
WEB_CONCURRENCY = 100
POOL_SIZE = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)

if "win" in sys.platform:
    # Set event loop policy for Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

connect_args = {"check_same_thread": False}

engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=False,
    future=True,
    pool_size=POOL_SIZE,
    # max_overflow=64,
    poolclass=QueuePool,  # Asincio pytest works with NullPool
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
