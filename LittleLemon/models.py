from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime,Enum
from sqlalchemy.orm import relationship
from database import Base

import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)  # role


class Menu(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    no_of_guests = Column(Integer)
    booking_date = Column(DateTime)
