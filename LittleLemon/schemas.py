from pydantic import BaseModel
from datetime import date
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class RegisterRequest(BaseModel):
    username: str
    password: str

class RegisterResponse(BaseModel):
    message: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "little_lemon_schema"}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)

class MenuBase(BaseModel):
    name: str
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


class MessageOut(BaseModel):
    message: str