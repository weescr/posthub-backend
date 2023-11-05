from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from .base import Base, engine, session_maker


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_session() -> AsyncSession:
    async with session_maker() as session:
        yield session


async def get_test_session() -> AsyncSession:
    async with session_maker() as session:
        yield session


@asynccontextmanager
async def get_session_context() -> AsyncSession:
    async with session_maker() as session:
        yield session
        await session.close()
