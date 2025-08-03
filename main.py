from fastapi import FastAPI, Query, Body, Path, HTTPException
from pydantic import BaseModel
from typing import Optional

hotels = [
    {'id': 0, 'title': 'Hilltop Inn', 'phone': 'Не указано'},
    {'id': 1, 'title': 'Atlantic Hotel', 'phone': '+1 410-641-3589'},
    {'id': 2, 'title': 'Comfort Inn & Suites Montpelier-Berlin', 'phone': '+1 802-613-1120'},
    {'id': 3, 'title': 'Days Inn', 'phone': '+1 860-438-6178'},
    {'id': 4, 'title': 'Best Western Plus', 'phone': '+1 860-828-3000'},
    {'id': 5, 'title': 'Homewood Suites by Hilton Boston Marlborough;Homewood Suites', 'phone': '+1 978-838-9940'},
    {'id': 6, 'title': 'New National Hotel', 'phone': '814 267-4815'},
]
app = FastAPI()

class HotelUpdate(BaseModel):
    title: Optional[str] = None
    phone: Optional[str] = None

@app.get("/hotels")
async def get_hotels(
    id_hotel: int | None = Query(None, description="The ID of the hotel."),
    title: str | None = Query(None, description="The title of the hotel."),
):
    hotels_ = []
    for hotel in hotels:
        if id_hotel and hotel['id'] != id_hotel:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_

@app.post("/hotels")
async def post_hotels(
        title: str = Body(embed=True, description="The title of the hotel."),
        phone: str = Body(embed=True, description="The phone of the hotel."),
):
    global hotels
    hotels.append({'id': hotels[-1]["id"] + 1,
                   'title': title,
                   'phone': phone})
    return {"Status": "OK"}

@app.put("/hotels/{id_hotel}")
async def put_hotels(
        id_hotel: int = Path(description="The ID of the hotel."),
        title: str = Body(embed=True, description="The title of the hotel."),
        phone: str = Body(embed=True, description="The phone of the hotel."),
):
    global hotels
    if any(hotel['id'] == id_hotel for hotel in hotels):
        hotels[id_hotel]["title"] = title
        hotels[id_hotel]["phone"] = phone
        return {"Status": "OK"}
    else:
        return {"Status": "ERROR", "message": f"The hotel `{id_hotel}` not found."}

@app.patch("/hotels/{id_hotel}")
async def patch_hotels(
        id_hotel: int = Path(description="The ID of the hotel."),
        hotel_data: HotelUpdate = Body(embed=True, description="The hotel data."),
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == id_hotel:
            data = hotel_data.model_dump(exclude_unset=True)
            hotel.update(data)
            return {"Status": "OK", "hotel": hotel}
    raise HTTPException(status_code=404, detail="The hotel does not exist.")

@app.delete("/hotels/{hotel_id}")
async def delete_hotel(hotel_id: int):
    global hotels
    hotels.remove(hotels[hotel_id])
    return {"status": "DELETED"}
