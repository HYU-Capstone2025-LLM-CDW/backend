from typing import Optional, Union
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

from src.validator.sql_validator.basic_sql_validator import BasicSQLValidator


class SqlExecutorRequestDto(BaseModel):
    sql: str = Field(..., title="SQL to execute on OMOP DB", description="The SQL to execute on OMOP DB")
    
    @field_validator("sql")
    def validate_text(cls, value):
        # try:
        #     BasicSQLValidator(value).validate()
        # except Exception as e:
        #     raise HTTPException(status_code=400, detail=str(e))
            
        return value
    
class SqlExecutorResponseDto(BaseModel):
    data: Optional[Union[list, dict]] = Field(None, title="Data", description="The data returned from the OMOP DB")
    error: Optional[str] = Field(None, title="Error", description="The error message if an error occurred")