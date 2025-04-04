from fastapi import APIRouter

from src.modules.sql_executor import service as sql_executor_service
from src.modules.sql_executor.dto import SqlExecutorRequestDto, SqlExecutorResponseDto


router = APIRouter(prefix="/sql-executor", tags=["Text to SQL"])


@router.post("/")
async def sql_executor(sqlExecutorRequestDto: SqlExecutorRequestDto) -> SqlExecutorResponseDto:
    return sql_executor_service.execute(sqlExecutorRequestDto)