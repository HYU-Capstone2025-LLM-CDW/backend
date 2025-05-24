from sqlalchemy.orm import Session
from src.modules.auth.dto import *
from src.modules.auth.model import User
from src.database import get_db_internal
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import List

from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import traceback

# hashing password
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


_bearer_scheme = HTTPBearer()

# JWT Config
_SECRET_KEY = "temp"
_ALGORITHM = "HS256"
_ACCESS_TOKEN_EXPIRE_MINUTE = 30

def hash_password(password : str) -> str:
    return _pwd_context.hash(password)


def verify_password(plain: str, hashed : str) -> bool:
    return _pwd_context.verify(plain, hashed)

# jwt token
# 추후에 refresh token 도입 필요성
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=_ACCESS_TOKEN_EXPIRE_MINUTE)
        
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, _SECRET_KEY, algorithm=_ALGORITHM)

# 현재 Login 한 user 받아오기
# Login 한 User 만 호출할 수 있는 API 일시 이 함수 router 매개변수로 넣을 것
def get_current_user(token: HTTPAuthorizationCredentials = Depends(_bearer_scheme)) -> dict:
    try :
        payload = jwt.decode(token.credentials, _SECRET_KEY, algorithms=[_ALGORITHM])
        return payload
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials.")
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An unexpected server error occurred during get current user.")

# 관리자 검증 함수
# 관리자만 호출 가능한 API 일시 이 함수 router 에 매개변수로 넣을 것
def get_current_admin_user(token : str = Depends(_bearer_scheme)) -> dict:
    try : 
        user = get_current_user(token)
        role = user.get("role")
        
        if role not in ("admin"):
            raise HTTPException(status_code=403, detail="Admin access required")
        return user
    
    
    except HTTPException as h:
        raise h
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An unexpected server error occurred in check admin user.")


# 회원 가입 함수
def create_user(userCreateRequestDto : UserCreateRequestDto,  db : Session) -> UserCreateResonseDto:
    try :
        # 이미 존재하는 지 확인
        existing = db.query(User).filter(
            (User.email == userCreateRequestDto.email)
            ).first()

        # 아래 except 에서 안 잡힘
        if existing : 
            raise HTTPException(status_code=400, detail="User already exists")
        
        db_user = User(
            email = userCreateRequestDto.email,
            employee_number = userCreateRequestDto.employee_number,
            password_hash = hash_password(userCreateRequestDto.password)
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return UserCreateResonseDto(text= "회원가입 요청 성공")
    
    except HTTPException as h:
        raise h
    
    except SQLAlchemyError as db_err:
        db.rollback()
        print(f"Database Error: {db_err}")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="An error occurred while executing the SQL query.")

    except Exception as e:
        db.rollback()
        print(f"Unexpected Error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")
    
    
# Login 함수
# Swagger 로 test 시 token 받아서 그대로 넣기
def login_user(userLoginRequestDto : UserLoginRequestDto, db : Session) -> str:
    try :
        user : User = db.query(User).filter(User.email == userLoginRequestDto.email).first()
    
        if not user or not verify_password(userLoginRequestDto.password_hash, user.password_hash):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        
        if not user.status == 'APPROVED':
            raise HTTPException(status_code=403, detail="User not approved by admin yet.")
        
        token_data = {
            "sub" : user.email,
            "role" : user.role
        }
        
        token = create_access_token(token_data)
        return token
    
    except HTTPException as h:
        traceback.print_exc()
        raise h
    
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")

# 관리자의 user 승인
def approve_user(userApproveRequestDto : UserApproveRequestDto, db : Session) -> UserApproveResponseDto:
    try : 
        user = db.query(User).filter(User.email == userApproveRequestDto.email).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.status = 'APPROVED'
        db.commit()
        
        return UserApproveResponseDto(text= "approve success")
    
    except HTTPException as h:
        raise h

    except SQLAlchemyError as db_err:
        db.rollback()
        print(f"Database Error: {db_err}")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="An error occurred while executing the SQL query.")

    except Exception as e:
        db.rollback()
        print(f"Unexpected Error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")

# 관리자의 유저 삭제
def delete_user(userDeleteRequestDto : UserDeleteRequestDto , db : Session) -> UserDeleteResponseDto:
    try:
        user = db.query(User).filter(User.email == userDeleteRequestDto.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        db.delete(user)
        db.commit()
        return UserDeleteResponseDto(text="Delete Success")

    except HTTPException as h:
        raise h

    except SQLAlchemyError as db_err:
        db.rollback()
        print(f"Database Error: {db_err}")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="An error occurred while executing the SQL query.")

    except Exception as e:
        db.rollback()
        print(f"Unexpected Error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")

# 관리자의 유저 조회 (비승인)
def get_unapproved_user(db : Session) -> List[User]:
    unapproved_users = db.query(User).filter(User.status == "PENDING").all()
    return unapproved_users


# admin 계정 만드는 코드
# 임시 코드
def add_admin_user():
    db = get_db_internal()
    
    try :
        admin_user = User(
            email ="admin",
            employee_number="admin",
            password_hash=hash_password("password"),  # 반드시 암호화
            status="APPROVED",
            role="admin"
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        db.close()
    
    except Exception as e:
        db.rollback()
        print("관리자 계정 생성 중 오류 발생")
        
# add_admin_user()