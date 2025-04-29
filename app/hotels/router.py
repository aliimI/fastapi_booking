import asyncio
from datetime import date, datetime
from typing import List

from fastapi_cache.decorator import cache
from pydantic import TypeAdapter

from app.exceptions import HotelNotFound, RoomsNotFound
from app.hotels.dao import HoletDAO
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRooms
from app.hotels.schemas import SHotels
from fastapi import APIRouter, Query

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

@router.get("/{location}")
# @cache(expire=20)
async def get_hotels_by_location_and_time(
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {datetime.now().date()}"),
):
    # await asyncio.sleep(3)
    hotels = await HoletDAO.search_for_hotels(location, date_from, date_to)
    hotels_list_adapter = TypeAdapter(List[SHotels])
    hotels_json = hotels_list_adapter.validate_python(hotels)
    if not hotels:
        raise HotelNotFound
    return hotels_json 

@router.get("/{hotel_id}/rooms", response_model=List[SRooms])
async def get_rooms_by_hotel_id(
    hotel_id: int,
    date_from: date = Query(..., description="Начало даты бронирования"),
    date_to: date = Query(..., description="Конец даты бронирования"),
    ):
    rooms = await RoomDAO.find_by_hotel_id(hotel_id)
    if not rooms:
        raise RoomsNotFound
    room_list = []

    for room in rooms:
        total_cost = (date_to - date_from).days * room.price  #оплата по дням
        rooms_left = room.quantity 

        room_info = {
            "id": room.id,
            "hotel_id": room.hotel_id,
            "name": room.name,
            "description": room.description,
            "services": room.services,
            "price": room.price,
            "quantity": room.quantity,
            "image_id": room.image_id,
            "total_cost": total_cost,
            "rooms_left": rooms_left,
        }
        room_list.append(room_info)

    return room_list


@router.get("id/{hotel_id}", response_model=SHotels)
async def get_hotel_by_id(hotel_id: int):
    hotel = await HoletDAO.find_by_id(hotel_id)
    if not hotel:
        raise HotelNotFound
    
    return hotel
