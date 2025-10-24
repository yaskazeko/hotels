from datetime import date
from typing import Optional, Sequence

from sqlalchemy import and_, delete, select, update, func
from sqlalchemy.ext.asyncio import AsyncSession


from src.models.booking import BookingsOrm
from src.models.rooms import RoomOrm



def rooms_ids_for_booking(
        date_from: date,
        date_to: date,
        hotel_id: int | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ):
    rooms_count = (
        select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsOrm)
        .filter(
            BookingsOrm.date_from <= date_to,
            BookingsOrm.date_to >= date_from,
        )
        .group_by(BookingsOrm.room_id)
        .cte(name="rooms_count")
    )
    rooms_left_table=(
        select(
            RoomOrm.id.label("room_id"),
            (RoomOrm.capacity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
        )
        .select_from(RoomOrm)
        .outerjoin(rooms_count, RoomOrm.id == rooms_count.c.room_id)
        .cte(name="rooms_left_table")
    )

    room_ids_for_hotel = (
        select(RoomOrm.id)
        .select_from(RoomOrm)
    )
    if hotel_id is not None:
        room_ids_for_hotel = room_ids_for_hotel.filter_by(hotel_id = hotel_id)

    room_ids_for_hotel = (
        room_ids_for_hotel
        .subquery(name="room_ids_for_hotel")
    )



    rooms_id_to_get = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(room_ids_for_hotel)
        )
        .offset(offset)
        .limit(limit)
    )
    return rooms_id_to_get