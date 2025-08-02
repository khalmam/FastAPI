from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, Food, Consume
from schemas import FoodCreate, ConsumeCreate, FoodOut, ConsumeOut
from typing import List

DATABASE_URL = "sqlite:///./calories.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Add Food
@app.post("/foods", response_model=FoodOut)
def add_food(food: FoodCreate, db: Session = Depends(get_db)):
    new_food = Food(name=food.name, calories=food.calories)
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return new_food

# ✅ List Foods
@app.get("/foods", response_model=List[FoodOut])
def get_foods(db: Session = Depends(get_db)):
    return db.query(Food).all()

# ✅ Add Consumed Food
@app.post("/consume", response_model=ConsumeOut)
def add_consumed(consumed: ConsumeCreate, db: Session = Depends(get_db)):
    food = db.query(Food).filter(Food.id == consumed.food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    entry = Consume(user_id=consumed.user_id, food=food)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

# ✅ Get Consumed by User
@app.get("/consume/{user_id}", response_model=List[ConsumeOut])
def get_consumed(user_id: int, db: Session = Depends(get_db)):
    return db.query(Consume).filter(Consume.user_id == user_id).all()

# ✅ Delete Consumed
@app.delete("/consume/{id}")
def delete_consumed(id: int, db: Session = Depends(get_db)):
    consumed = db.query(Consume).filter(Consume.id == id).first()
    if not consumed:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(consumed)
    db.commit()
    return {"message": "Deleted successfully"}
