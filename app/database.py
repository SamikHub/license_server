from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    future=True,
    echo=False,  # можна увімкнути True для дебагу SQL
)

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    future=True
)

# Функція для отримання сесії з залежностей
async def get_db():
    async with async_session() as session:
        yield session