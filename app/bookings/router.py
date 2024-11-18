from datetime import date
from fastapi import APIRouter, Depends, Request

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import RoomCannotBeBooked
from app.exceptions import BookingNotFound
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(
    user: Users = Depends(get_current_user)
    ) -> list[SBooking]:
    return  await BookingDAO.find_all(user_id=user.id)


@router.post("")
async def add_booking(
    room_id: int, 
    date_from: date, 
    date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    return {"detail": "Booking successful", "booking": booking}

    
@router.delete("")
async def remove_booking(
    room_id: int,
    user: Users = Depends(get_current_user),
):
    rows_deleted = await BookingDAO.delete_booking(room_id=room_id, user_id=user.id)
    if rows_deleted == 0:
        raise BookingNotFound
    return {"detail": "Бронь успешно удалена!"}