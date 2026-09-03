from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = "sqlite+aiosqlite:///./genai.db"


engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def init_db() -> None:
    async with engine.begin() as connection:

        # Documents table
        await connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    content TEXT NOT NULL
                )
                """
            )
        )

        # Request logs table
        await connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS request_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    request_id TEXT NOT NULL,
                    endpoint TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    total_latency_ms REAL,
                    model_version TEXT,
                    prompt_version TEXT,
                    outcome TEXT,
                    error_category TEXT
                )
                """
            )
        )

        # Retrieved source logs table
        await connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS retrieved_source_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    request_id TEXT NOT NULL,
                    source_id TEXT NOT NULL,
                    score REAL,
                    created_at TEXT NOT NULL
                )
                """
            )
        )


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session