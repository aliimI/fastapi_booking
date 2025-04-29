from sqlalchemy import select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_by_hotel_id(cls, hotel_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.hotel_id == hotel_id)
            result = await session.execute(query)
            return result.mappings().all()