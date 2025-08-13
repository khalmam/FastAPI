from fastapi import Depends, APIRouter
from typing import List

from core.utils import get_current_user
from core.exceptions import ForbiddenException
from schemas import MenuOut

def admin_required(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise ForbiddenException("Admins only")
    return current_user

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.get("/", response_model=List[MenuOut])
async def get_menu_items(current_user=Depends(admin_required)):
    # ...your logic to fetch menu items...
    pass