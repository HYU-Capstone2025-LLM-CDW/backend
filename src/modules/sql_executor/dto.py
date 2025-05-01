from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

from src.validator.sql_validator.basic_sql_validator import BasicSQLValidator   # 기본 검증
from src.validator.sql_validator.safety_sql_validator import SQLComplexityLimiter  # 쿼리 복잡도 제한
from src.validator.sql_validator.secure_sql_validator import SQLSecurityValidator # 민감정보 보호


class SqlExecutorRequestDto(BaseModel):
    sql: str = Field(..., title="SQL to execute on OMOP DB", description="The SQL to execute on OMOP DB")
    
    @field_validator("sql")
    def validate_text(cls, value):
        try:
            # 쿼리 기본 검증
            BasicSQLValidator(value).validate()
            # 쿼리 복잡도 검사
            SQLComplexityLimiter(value).validate()
            #쿼리 민감 정보 보호
            SQLSecurityValidator(value).validate()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
            
        return value
    
class SqlExecutorResponseDto(BaseModel):
    data: Optional[dict] = Field(None, title="Data", description="The data returned from the OMOP DB")
    error: Optional[str] = Field(None, title="Error", description="The error message if an error occurred")