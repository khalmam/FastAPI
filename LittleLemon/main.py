from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import Base, engine
from routers import menu, booking, pages
from routers import auth  #  Import your auth router

from fastapi import FastAPI
from exceptions import validation_exception_handler, http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

app = FastAPI()

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)


# This line ensures all tables defined in your models are created.
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Little Lemon API")

# Configure Jinja2Templates to use your templates directory
templates = Jinja2Templates(directory="templates")

# Mount the static directory to serve CSS, images, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include Routers
app.include_router(auth.router)  
app.include_router(menu.router)
app.include_router(booking.router)
app.include_router(pages.router)
