from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Menu, User
from schemas import MenuCreate,MenuOut,MenuBase
from typing import List
from routers.auth import get_current_user
from exceptions import UnauthorizedException, ForbiddenException, NotFoundException

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.get("/", response_model=List[MenuOut])
def get_menu_items(db: Session = Depends(get_db)):
    return db.query(Menu).all()

@router.post("/", response_model=MenuOut)
def create_menu_item(
    item: MenuCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)   # ✅ Requires JWT
):
    new_item = Menu(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/{item_id}", response_model=MenuOut)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Menu).filter(Menu.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

# @router.delete("/{item_id}")
# def delete_menu_item(
#     item_id: int,
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user)   # ✅ Requires JWT
# ):
#     item = db.query(Menu).filter(Menu.id == item_id).first()
#     if not item:
#         raise HTTPException(status_code=404, detail="Menu item not found")
#     db.delete(item)
#     db.commit()
#     return {"message": "Deleted successfully"}

@router.delete("/{item_id}")
def delete_menu_item(item_id: int, 
                     db: Session = Depends(get_db), 
                     current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise UnauthorizedException("Admins only")
    
    item = db.query(Menu).filter(Menu.id == item_id).first()
    if not item:
        raise NotFoundException("Menu item not found")
    
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}
