from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo

class UserCreateRequestDto(BaseModel):
    employee_id: str
    password: str
    password_verification : str
    
    @field_validator('employee_id', 'password', 'password_verification')
    def not_empty(cls, v : str):
        if not v or not v.strip():
            raise ValueError('빈 값 허용 안 됨')
        return v
    
    @field_validator('password_verification')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v   
    
    
class UserLoginRequestDto(BaseModel):
    employee_id : str
    password : str

class UserApproveRequestDto(BaseModel):
    employee_id : str

class UserDeleteRequestDto(BaseModel):
    employee_id : str


class UserOutResponseDto(BaseModel):
    id : int
    employee_id : str
    is_approved: bool
    role : str
    
    class Config:
        from_attributes = True 




class UserCreateResonseDto(BaseModel):
    text : str

class UserLoginResonseDto(BaseModel):
    access_token: str
    token_type : str
    
class UserApproveResponseDto(BaseModel):
    text : str
    
class UserDeleteResponseDto(BaseModel):
    text : str