from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Menu
from schemas import MenuCreate, MenuOut,MessageOut
from typing import List
from core.dependencies import admin_required   
from routers.auth import get_current_user
from core.exceptions import NotFoundException

router = APIRouter(prefix="/menu", tags=["Menu"])

# Public route
@router.get("/", response_model=List[MenuOut])
def get_menu_items(db: Session = Depends(get_db)):
    return db.query(Menu).all()

# Protected (any authenticated user)
@router.post("/", response_model=MenuOut)
def create_menu_item(
    item: MenuCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_item = Menu(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# Public route
@router.get("/{item_id}", response_model=MenuOut)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Menu).filter(Menu.id == item_id).first()
    if not item:
        raise NotFoundException("Menu item not found")
    return item

# Protected (admin only)
@router.put("/{item_id}", response_model=MenuOut)
def update_menu_item(
    item_id: int,
    item: MenuCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    existing_item = db.query(Menu).filter(Menu.id == item_id).first()
    if not existing_item:
        raise NotFoundException("Menu item not found")
    for key, value in item.dict().items():
        setattr(existing_item, key, value)
    db.commit()
    db.refresh(existing_item)
    return existing_item

@router.delete("/{item_id}", response_model=MessageOut)
def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    item = db.query(Menu).filter(Menu.id == item_id).first()
    if not item:
        raise NotFoundException("Menu item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}