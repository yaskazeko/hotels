

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class RoomsOrm(Base):
    __tablename__ = 'rooms'
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str] = mapped_column(String(100))
    discription: Mapped[str | None] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(default=0)
    floor: Mapped[str] = mapped_column(default=1)
    quantity: Mapped[int] = mapped_column(default=0)
