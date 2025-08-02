from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Food, Consume
from schemas import FoodCreate, ConsumeCreate
from typing import List

DATABASE_URL = "sqlite:///./calories.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Render index page
@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    foods = db.query(Food).all()
    consumed_food = db.query(Consume).all()
    return templates.TemplateResponse("index.html", {"request": request, "foods": foods, "consumed_food": consumed_food})

# ✅ Handle food consumption form
@app.post("/consume")
def add_consumed(request: Request, food_id: int = Form(...), user_id: int = Form(1), db: Session = Depends(get_db)):
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    entry = Consume(user_id=user_id, food=food)
    db.add(entry)
    db.commit()
    return RedirectResponse("/", status_code=303)

# ✅ Delete consumed food
@app.get("/delete/{id}")
def delete_page(request: Request, id: int):
    return templates.TemplateResponse("delete.html", {"request": request, "id": id})

@app.post("/delete/{id}")
def delete_consumed(id: int, db: Session = Depends(get_db)):
    consumed = db.query(Consume).filter(Consume.id == id).first()
    if not consumed:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(consumed)
    db.commit()
    return RedirectResponse("/", status_code=303)
