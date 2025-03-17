from fastapi import APIRouter

from src.modules.text_to_sql.dto import TextToSQLRequestDto
from src.modules.text_to_sql import service as text_to_sql_service

router = APIRouter(prefix="/text-to-sql", tags=["text-to-sql"])

@router.get("/")
async def health_check():
    return {"status": "ok"}

@router.post("/")
async def text_to_sql(body: TextToSQLRequestDto):
    return text_to_sql_service.convert_text_to_sql(body)
