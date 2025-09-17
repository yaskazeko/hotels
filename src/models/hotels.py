
from __future__ import annotations

from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class HotelsOrm(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20))
    location: Mapped[str] = mapped_column(String(200))


    rooms: Mapped[List["RoomOrm"]] = relationship(
        back_populates="hotel", cascade="all, delete-orphan"
    )


