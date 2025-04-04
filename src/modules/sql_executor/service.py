from src.modules.sql_executor.dto import SqlExecutorRequestDto, SqlExecutorResponseDto


def execute(sqlExecutorRequestDto: SqlExecutorRequestDto) -> SqlExecutorResponseDto:
    return SqlExecutorResponseDto(data=None, error=None)