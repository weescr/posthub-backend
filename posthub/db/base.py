from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from posthub.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

Base = declarative_base()
session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
