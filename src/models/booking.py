from sqlalchemy import Integer, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from src.database import Base





class BookingsOrm(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[float]

    @hybrid_property
    def total_price(self) -> float:
        return self.price * (self.date_to - self.date_from).days
