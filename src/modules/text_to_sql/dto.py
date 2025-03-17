from pydantic import BaseModel


class TextToSQLRequestDto(BaseModel):
    text: str
    
class TextToSQLResponseDto(BaseModel):
    sql: str
    