from typing import Optional

from pydantic import BaseModel, ConfigDict


class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: str
    quantity: int
    image_id: int
    total_cost: Optional[int] = None  # Total cost for the booking period
    rooms_left: Optional[int] = None   # Remaining number of available rooms

    model_config = ConfigDict(from_attributes=True)