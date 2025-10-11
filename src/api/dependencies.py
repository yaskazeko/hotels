from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel

from src.database import async_session_maker
from src.utils.db_manager import DBManager

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="The page number of the hotel.")]
    per_page: Annotated[int | None, Query(3, ge=3, le=10, description="The number of items per page.")]

PaginationDep = Annotated[PaginationParams, Depends()]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)

async def get_db():
    async with get_db_manager() as db:
        yield db



DBDep: type[DBManager] = Annotated[DBManager, Depends(get_db)]