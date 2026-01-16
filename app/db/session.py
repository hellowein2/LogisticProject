from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


sync_engine = create_engine(settings.DATABASE_URL_SYNC,pool_pre_ping=True)
SessionLocal = sessionmaker(bind=sync_engine)



async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
