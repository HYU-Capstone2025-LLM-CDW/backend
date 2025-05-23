from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db

from src.modules.auth.dto import *
from src.modules.auth.service import create_user, login_user, get_current_admin_user, approve_user, get_unapproved_user, delete_user

router = APIRouter(prefix="/auth", tags=["Text to SQL"])

# GET

@router.get("/unapproved", response_model=list[UserOutResponseDto])
def get_unapproved(db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user)) -> list[UserOutResponseDto]:
    return get_unapproved_user(db)

# POST

@router.post("/signup")
def signup(userCreateRequestDto : UserCreateRequestDto, db : Session = Depends(get_db)) -> UserCreateResonseDto:
    return create_user(userCreateRequestDto, db)

@router.post("/login", response_model=UserLoginResonseDto)
def login(userLoginRequestDto : UserLoginRequestDto,  db : Session = Depends(get_db)) -> UserLoginResonseDto:
    token = login_user(userLoginRequestDto, db)
    return UserLoginResonseDto(access_token = token, token_type = "Bearer")


@router.post("/approve", response_model=UserApproveResponseDto)
def approve(userApproveRequestDto : UserApproveRequestDto, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user)) -> UserApproveResponseDto:
    return approve_user(userApproveRequestDto, db)


# DELETE

@router.delete("/user", response_model=UserDeleteResponseDto)
def delete(userDeleteRequestDto : UserDeleteRequestDto, db : Session = Depends(get_db), user: dict = Depends(get_current_admin_user)) -> UserDeleteResponseDto:
    return delete_user(userDeleteRequestDto, db)