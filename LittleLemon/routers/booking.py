from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Booking
from schemas import BookingCreate, BookingOut
from typing import List
from routers.auth import get_current_user   #  import JWT dependency

router = APIRouter(prefix="/bookings", tags=["Booking"])

@router.get("/", response_model=List[BookingOut])
def list_bookings(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)   #  require login for viewing all bookings
):
    return db.query(Booking).all()

@router.post("/", response_model=BookingOut)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)  
):
    new_booking = Booking(**booking.dict())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking
