from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, Query, status
from pydantic import BaseModel

from src.database import async_session_maker
from src.services.auth import AuthService
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


async def get_current_user_id(
    access_token: Annotated[str | None, Cookie()] = None
) -> int:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required"
        )

    payload = AuthService.decode_access_token(access_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    return user_id


DBDep: type[DBManager] = Annotated[DBManager, Depends(get_db)]
CurrentUserDep = Annotated[int, Depends(get_current_user_id)]