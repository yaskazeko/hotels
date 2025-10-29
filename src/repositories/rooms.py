from datetime import date
from typing import Optional, Sequence

from sqlalchemy import and_, delete, select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import engine
from src.models.booking import BookingsOrm
from src.models.rooms import RoomOrm
from src.schemes.rooms import RoomCreate, RoomUpdate


class RoomsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, room_id: int) -> Optional[RoomOrm]:
        res = await self.session.execute(select(RoomOrm).where(RoomOrm.id == room_id))
        return res.scalar_one_or_none()

    async def get_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,

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
            .filter_by(hotel_id=hotel_id)
            .subquery(name="room_ids_for_hotel")
        )

        rooms_is_to_get = (
            select(rooms_left_table)
            .select_from(rooms_left_table)
            .filter(rooms_left_table.c.rooms_left > 0,
                    rooms_left_table.c.room_id.in_(room_ids_for_hotel)
            )
        )
        return await self.get_filtered(RoomOrm.id.in_(rooms_is_to_get))

    async def list(
        self,
        *,
        hotel_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        capacity: Optional[int] = None,
        is_active: Optional[bool] = True,
        limit: int = 50,
        offset: int = 0,
        order_by_price: Optional[str] = None,  # "asc" | "desc"
    ) -> Sequence[RoomOrm]:
        conds = []
        if hotel_id is not None:
            conds.append(RoomOrm.hotel_id == hotel_id)
        if is_active is not None:
            conds.append(RoomOrm.is_active == is_active)
        if capacity is not None:
            conds.append(RoomOrm.capacity >= capacity)
        if min_price is not None:
            conds.append(RoomOrm.price_per_night >= min_price)
        if max_price is not None:
            conds.append(RoomOrm.price_per_night <= max_price)

        stmt = select(RoomOrm).where(and_(*conds)) if conds else select(RoomOrm)

        if order_by_price == "asc":
            stmt = stmt.order_by(RoomOrm.price_per_night.asc())
        elif order_by_price == "desc":
            stmt = stmt.order_by(RoomOrm.price_per_night.desc())

        stmt = stmt.limit(limit).offset(offset)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def create(self, data: RoomCreate) -> RoomOrm:
        room = RoomOrm(**data.model_dump(exclude={'facilities_ids'}))
        self.session.add(room)
        await self.session.flush()  # чтобы получить room.id
        return room

    async def update(self, room_id: int, data: RoomUpdate) -> Optional[RoomOrm]:
        payload = {k:v for k,v in data.model_dump(exclude_unset=True, exclude={'facilities_ids'}).items()}
        if not payload:
            return await self.get_by_id(room_id)

        await self.session.execute(
            update(RoomOrm).where(RoomOrm.id == room_id).values(**payload)
        )
        await self.session.flush()
        return await self.get_by_id(room_id)

    async def delete(self, room_id: int) -> bool:
        await self.session.execute(delete(RoomOrm).where(RoomOrm.id == room_id))

        return True