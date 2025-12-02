import json

from fastapi import APIRouter, HTTPException, status
from starlette.responses import JSONResponse

from src.api.dependencies import CurrentUserDep, DBDep
from src.init import redis_manager
from src.schemes.facilities import FacilitiesAdd, Facility

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("/{facility_id}")
async def get_facility(
    facility_id: int,
    db: DBDep,
):
    facility_from_cash = await redis_manager.get(f"facility:{facility_id}")
    if facility_from_cash:
        return json.loads(facility_from_cash)

    facility_orm = await db.facilities.get(facility_id)
    if not facility_orm:
        raise HTTPException(status_code=404, detail="Facility not found")

    facility_schema = Facility.model_validate(facility_orm)
    facility_json = facility_schema.model_dump_json()
    await redis_manager.set(f"facility:{facility_id}", facility_json, expire=3600)

    return facility_schema


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_facility(
    data: FacilitiesAdd,
    db: DBDep,
):
    facility = await db.facilities.create(data)
    await db.commit()
    return facility
