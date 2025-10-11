from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.models.users import UsersOrm
    from src.models.rooms import RoomOrm


class BookingsOrm(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), index=True)
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[float] = mapped_column(Numeric(10, 2))

    # Relationships
    user: Mapped["UsersOrm"] = relationship(back_populates="bookings")
    room: Mapped["RoomOrm"] = relationship(back_populates="bookings")

    @hybrid_property
    def total_price(self) -> float:
        return float(self.price * (self.date_to - self.date_from).days)

    @hybrid_property
    def total_days(self) -> int:
        return (self.date_to - self.date_from).days
