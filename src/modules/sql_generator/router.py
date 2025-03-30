from fastapi import APIRouter

from src.modules.sql_generator.dto import SqlGeneratorRequestDto
from src.modules.sql_generator import service as sql_generator_service

router = APIRouter(prefix="/sql-generator", tags=["sql-generator"])

@router.post("/")
async def text_to_sql(body: SqlGeneratorRequestDto):
    return sql_generator_service.convert_text_to_sql(body)
