from sqlalchemy.orm import Session
from src.modules.auth.dto import UserCreateRequestDto, UserLoginRequestDto, UserCreateResonseDto
from src.modules.auth.model import User
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
import traceback

# hashing password
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# JWT Config
_SECRET_KEY = "temp"
_ALGORITHM = "HS256"
_ACCESS_TOKEN_EXPIRE_MINUTE = 30

def hash_password(password : str) -> str:
    return _pwd_context.hash(password)


def verify_password(plain: str, hashed : str) -> bool:
    return _pwd_context.verify(plain, hashed)

# jwt token
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=_ACCESS_TOKEN_EXPIRE_MINUTE)
        
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, _SECRET_KEY, algorithm=_ALGORITHM)


def get_current_user(token: str = Depends(_oauth2_scheme)) -> dict:
    try :
        payload = jwt.decode(token, _SECRET_KEY, algorithms=[_ALGORITHM])
        return payload
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")

# 관리자 검증 함수
def get_current_admin_user(token : str = Depends(_oauth2_scheme)) -> dict:
    try : 
        user = get_current_user(token)
        role = user.get("role")
        
        if role not in ("admin"):
            raise HTTPException(status_code=403, detail="Admin access required")
        return user

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")


# signup
def create_user(userCreateRequestDto : UserCreateRequestDto,  db : Session) -> UserCreateResonseDto:
    try :
        # 이미 존재하는 지 확인
        existing = db.query(User).filter(
            (User.employee_id == userCreateRequestDto.employee_id)
            ).first()

        # 아래 except 에서 안 잡힘
        if existing : 
            raise HTTPException(status_code=400, detail="User already exists")
        
        db_user = User(
            employee_id = userCreateRequestDto.employee_id,
            password = hash_password(userCreateRequestDto.password)
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return UserCreateResonseDto(text= "회원가입 성공")
        
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
    
    
# Login 기능
def login_user(userLoginRequestDto : UserLoginRequestDto, db : Session) -> str:
    try :
        user : User = db.query(User).filter(User.employee_id == userLoginRequestDto.employee_id).first()
    
        if not user or not verify_password(userLoginRequestDto.password, user.password):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        
        if not user.is_approved:
            raise HTTPException(status_code=403, detail="User not approved by admin yet.")
        
        token_data = {
            "sub" : user.employee_id,
            "role" : user.role
        }
        
        
        token = create_access_token(token_data)
        return token
        
    
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

# 관리자의 user 승인
def approve_user(user_id : int, db : Session) -> User:
    try : 
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_approved = True
        db.commit()
        

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