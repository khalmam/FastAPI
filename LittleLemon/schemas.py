from pydantic import BaseModel
from datetime import date

class MenuBase(BaseModel):
    title: str
    price: int
    description: str | None = None

class MenuCreate(MenuBase):
    pass

class MenuOut(MenuBase):
    id: int
    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    name: str
    guests: int
    date: date

class BookingCreate(BookingBase):
    pass

class BookingOut(BookingBase):
    id: int
    class Config:
        from_attributes = True
