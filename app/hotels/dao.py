from datetime import date
from typing import List

from sqlalchemy import and_, select
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker


class HoletDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(
        cls,
        name: str,
        location: str,
        services: str,
        rooms_quantity: int,
        image_id: int
    ):
        pass

    
    @classmethod
    async def find_by_location_and_availability(
            cls, location: str, date_from: date, date_to: date
    ) -> List[Hotels]:
        async with async_session_maker() as session:
            # Find hotels with available rooms during the given date range
            booked_rooms = select(Bookings.room_id).where(
                and_(
                    Bookings.date_from < date_to,
                    Bookings.date_to > date_from
                )
            ).cte("booked_rooms")

            query = (
                select(Hotels)
                .join(Rooms, Rooms.hotel_id == Hotels.id)
                .join(
                    booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                )
                .where(
                    and_(
                        Hotels.location.ilike(f"%{location}%"),
                        booked_rooms.c.room_id.is_(None)  # Only available rooms
                    )
                )
                .group_by(Hotels.id)
            )

            result = await session.execute(query)
            return result.scalars().all()