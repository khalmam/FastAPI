from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import Base, engine
from routers import menu, booking, pages

# This line ensures all tables defined in your models are created.
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Little Lemon API")

# Configure Jinja2Templates to use your templates directory
templates = Jinja2Templates(directory="templates")

# Mount the static directory to serve CSS, images, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include Routers
app.include_router(menu.router)
app.include_router(booking.router)
app.include_router(pages.router)