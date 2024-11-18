from app.database import Base
from sqlalchemy import JSON, Column, Computed, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]