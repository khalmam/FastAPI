from fastapi import Depends
from core.utils import get_current_user
from core.exceptions import ForbiddenException
from fastapi import APIRouter
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from schemas import  MenuOut
from .utils import get_current_user
from typing import List


router = APIRouter(prefix="/menu", tags=["Menu"])

@router.get("/", response_model=List[MenuOut])  


def admin_required(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise ForbiddenException("Admins only")
    return current_user