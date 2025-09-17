from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="The page number of the hotel.")]
    per_page: Annotated[int | None, Query(3, ge=3, le=10, description="The number of items per page.")]

PaginationDep = Annotated[PaginationParams, Depends()]