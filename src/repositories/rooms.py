from typing import Optional, Sequence

from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.rooms import RoomOrm
from src.schemes.rooms import RoomCreate, RoomUpdate


class RoomsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, room_id: int) -> Optional[RoomOrm]:
        res = await self.session.execute(select(RoomOrm).where(RoomOrm.id == room_id))
        return res.scalar_one_or_none()

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
        room = RoomOrm(**data.model_dump())
        self.session.add(room)
        await self.session.flush()  # чтобы получить room.id
        return room

    async def update(self, room_id: int, data: RoomUpdate) -> Optional[RoomOrm]:
        payload = {k:v for k,v in data.model_dump(exclude_unset=True).items()}
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