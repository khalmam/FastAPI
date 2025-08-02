from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    calories = Column(Integer)

class Consume(Base):
    __tablename__ = "consumes"

    id = Column (Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    food_id = Column(Integer, ForeignKey("foods.id"))
    food = relationship("Food")