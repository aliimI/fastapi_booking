from typing import TYPE_CHECKING

from sqlalchemy import JSON, Column, Computed, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from bookings.models import Bookings

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]

    # booking = relationship("Bookings", back_populates="user")
    bookings: Mapped[list["Bookings"]] = relationship(back_populates="user")

    def __str__(self):
        return f"User {self.email}"