from sqlalchemy.orm import Session
from src.modules.sql_executor.dto import SqlExecutorRequestDto, SqlExecutorResponseDto
from src.modules.omop.database import get_omop_data

async def execute(
    sqlExecutorRequestDto: SqlExecutorRequestDto,
) -> SqlExecutorResponseDto:
    try:
        data = get_omop_data(sqlExecutorRequestDto.sql)
        return SqlExecutorResponseDto(data=data)
    except Exception as e:
        return SqlExecutorResponseDto(error=str(e))
