from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db

from src.modules.auth.dto import UserCreateRequestDto, UserCreateResonseDto, UserLoginRequestDto, UserLoginResonseDto
from src.modules.auth.service import create_user, login_user, get_current_admin_user, approve_user

router = APIRouter(prefix="/auth", tags=["Text to SQL"])

@router.post("/signup")
def signup(userCreateRequestDto : UserCreateRequestDto, db : Session = Depends(get_db)) -> UserCreateResonseDto:
    return create_user(userCreateRequestDto, db)

@router.post("/login")
def login(userLoginRequestDto : UserLoginRequestDto,  db : Session = Depends(get_db)) -> UserLoginResonseDto:
    token = login_user(userLoginRequestDto, db)
    return UserLoginResonseDto(access_token = token, token_type = " bearer")

# 추후 dto 로 변경

@router.post("/approve/{user_id}")
def approve(user_id : int, db: Session = Depends(get_db), _: dict = Depends(get_current_admin_user)):
    user = approve_user(user_id, db)
