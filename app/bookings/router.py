from datetime import date

from pydantic import TypeAdapter
from fastapi_versioning import version

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import BookingNotFound, RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users
from fastapi import APIRouter, Depends, Request

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
@version(1)
async def get_bookings(
    user: Users = Depends(get_current_user)
    ) -> list[SBooking]:
    return  await BookingDAO.find_all(user_id=user.id)


@router.post("")
@version(1)
async def add_booking(
    room_id: int, 
    date_from: date, 
    date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    #validate_python converts an orm obj into SBooking pydanting model
    booking_dict = TypeAdapter(SBooking).validate_python(booking).model_dump() #pydantic v2 version of parse_obj_as
    
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict

    
@router.delete("")
@version(1)
async def remove_booking(
    room_id: int,
    user: Users = Depends(get_current_user),
):
    rows_deleted = await BookingDAO.delete_booking(room_id=room_id, user_id=user.id)
    if rows_deleted == 0:
        raise BookingNotFound
    return {"detail": "Бронь успешно удалена!"}