

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class HotelsOrm(Base):
    __tablename__ = 'hotels'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20))
    location: Mapped[str] = mapped_column(String(200))
