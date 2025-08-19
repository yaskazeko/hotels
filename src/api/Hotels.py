from fastapi import Query, Body, Path, HTTPException, APIRouter
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.api.Dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.schemes.hotel import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Hotels"])

hotels = [
    {'id': 0, 'title': 'Hilltop Inn', 'phone': 'Не указано'},
    {'id': 1, 'title': 'Atlantic Hotel', 'phone': '+1 410-641-3589'},
    {'id': 2, 'title': 'Comfort Inn & Suites Montpelier-Berlin', 'phone': '+1 802-613-1120'},
    {'id': 3, 'title': 'Days Inn', 'phone': '+1 860-438-6178'},
    {'id': 4, 'title': 'Best Western Plus', 'phone': '+1 860-828-3000'},
    {'id': 5, 'title': 'Homewood Suites by Hilton Boston Marlborough;Homewood Suites', 'phone': '+1 978-838-9940'},
    {'id': 6, 'title': 'New National Hotel', 'phone': '814 267-4815'},
]



@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    # id_hotel: int | None = Query(None, description="The ID of the hotel."),
    title: str | None = Query(None, description="The title of the hotel."),
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all_hotels(
            title=title,
            limit=pagination.per_page,
            offset=(pagination.page - 1)*pagination.per_page,
        )

@router.post("")
async def post_hotels(
        hotel_data: Hotel = Body(description="The hotel data.", openapi_examples={
            "1":{
                "summary": "Hotel 1",
                "value": {
                    "title": "Hilltop Inn",
                    "phone": "Не указано",
                    "location": "Berlin",
                },
            },
            "2":{
                "summary": "Hotel 2",
                "value": {
                    "title": "Atlantic Hotel",
                    "location": "Berlin",
                    "phone": "+1 410-641-3589",
                },
            },
            "3":{
                "summary": "Hotel 3",
                "value": {
                    "title": "Comfort Inn & Suites Montpelier-Berlin",
                    "location": "Berlin",
                    "phone": "+1 802-613-1120",
                },
            },
            "4":{
                "summary": "Hotel 4",
                "value": {
                    "title": "Days Inn",
                    "location": "Berlin",
                    "phone": "+1 860-438-6178",
                },
            },
            "5":{
                "summary": "Hotel 5",
                "value": {
                    "title": "Best Western Plus",
                    "location": "Berlin",
                    "phone": "+1 860-828-3000",
                },
            },
            "6":{
                "summary": "Hotel 6",
                "value": {
                    "title": "Homewood Suites by Hilton Boston Marlborough;Homewood Suites",
                    "location": "Berlin",
                    "phone": "+1 978-838-9940",
                },
            },
        })
):
    async with async_session_maker() as session:
        repo = HotelsRepository(session)
        try:
            obj = await repo.post_hotels(hotel_data)
            await session.flush()
            await session.refresh(obj)
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Hotel already exists or violates a constraint.",
            )
    return {
        "status": "OK",
    }



@router.put("/{id_hotel}")
async def put_hotels(
        id_hotel: int = Path(description="The ID of the hotel."),
        hotel_data: Hotel = Body(embed=True, description="The hotel data."),
):
    global hotels
    if any(hotel['id'] == id_hotel for hotel in hotels):
        hotels[id_hotel]["title"] = hotel_data.title
        hotels[id_hotel]["phone"] = hotel_data.phone
        return {"Status": "OK"}
    else:
        return {"Status": "ERROR", "message": f"The hotel `{id_hotel}` not found."}

@router.patch("/{id_hotel}")
async def patch_hotels(
        id_hotel: int = Path(description="The ID of the hotel."),
        hotel_data: HotelPatch = Body(embed=True, description="The hotel data."),
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == id_hotel:
            data = hotel_data.model_dump(exclude_unset=True)
            hotel.update(data)
            return {"Status": "OK", "hotel": hotel}
    raise HTTPException(status_code=404, detail="The hotel does not exist.")

@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    global hotels
    hotels.remove(hotels[hotel_id])
    return {"status": "DELETED"}