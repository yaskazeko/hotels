from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from config import settings

engine = create_async_engine(settings.db_url)

class Base(DeclarativeBase):
    pass
