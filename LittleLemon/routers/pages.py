from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import Booking

templates = Jinja2Templates(directory="templates")
router = APIRouter(tags=["Pages"])

@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@router.get("/reservations", response_class=HTMLResponse)
def reservations(request: Request, db: Session = Depends(get_db)):
    bookings = db.query(Booking).all()
    return templates.TemplateResponse("reservations.html", {"request": request, "bookings": bookings})
