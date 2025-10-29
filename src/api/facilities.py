from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import CurrentUserDep, DBDep
from src.schemes.facilities import FacilitiesBase

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("/{facility_id}")
async def get_facility(
    facility_id: int,
    db: DBDep,
):
    facility = await db.facilities.get(facility_id)
    if not facility:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Facility not found")
    return facility


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_facility(
    data: FacilitiesBase,
    db: DBDep,
):
    facility = await db.facilities.create(data)
    await db.commit()
    return facility