from fastapi import APIRouter, Depends

from src.modules.sql_generator.dto import SqlGeneratorRequestDto, SqlGeneratorResponseDto
from src.modules.sql_generator import service as sql_generator_service
from src.modules.auth.service import get_current_user

router = APIRouter(prefix="/sql-generator", tags=["Text to SQL"])

@router.post("/")
async def text_to_sql(body: SqlGeneratorRequestDto, user: dict = Depends(get_current_user)) -> SqlGeneratorResponseDto:
    return sql_generator_service.generate(body)
