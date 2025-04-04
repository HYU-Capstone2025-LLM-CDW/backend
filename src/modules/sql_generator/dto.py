from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

from src.validator.text_validator.basic_text_validator import BasicTextValidator
from src.validator.text_validator.secure_text_validator import SecureTextValidator
from src.validator.sql_validator.basic_sql_validator import BasicSQLValidator


class SqlGeneratorRequestDto(BaseModel):
    text: str = Field(..., title="Text to convert to SQL", description="The text to convert to SQL")
    
    @field_validator("text")
    def validate_text(cls, value):
        try:
            BasicTextValidator(value).validate()
            SecureTextValidator(value).validate()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
            
        return value
    
class SqlGeneratorResponseDto(BaseModel):
    sql: Optional[str] = Field(None, title="SQL", description="The generated SQL")
    error: Optional[str] = Field(None, title="Error", description="The error message if an error occurred")