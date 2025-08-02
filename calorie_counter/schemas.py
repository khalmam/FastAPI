from pydantic import BaseModel

class FoodCreate(BaseModel):
    name: str
    calories: int

class FoodOut(BaseModel):
    id: int
    name: str
    calories: str

    class Config:
        from_attributes = True



class ConsumeCreate(BaseModel):
    user_id: int
    food_id: int


class ConsumeOut(BaseModel):
    id: int
    user_id:int
    food: FoodOut
    
    class Config:
        from_attributes = True
