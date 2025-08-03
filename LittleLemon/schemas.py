from pydantic import BaseModel
from datetime import datetime

class MenuItemBase(BaseModel):
    name: str
    description: str
    price: float

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemOut(MenuItemBase):
    id: int
    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    name: str
    no_of_guests: int
    booking_date: datetime

class BookingCreate(BookingBase):
    pass

class BookingOut(BookingBase):
    id: int
    class Config:
        from_attributes = True
