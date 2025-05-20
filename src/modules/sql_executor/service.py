from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from datetime import datetime
from src.modules.sql_executor.dto import SqlExecutorRequestDto, SqlExecutorResponseDto
from src.modules.log.service import save_sql_executor_log
from src.modules.log.dto import SqlExecutorLogRequestModel
import traceback

async def execute(
    sqlExecutorRequestDto: SqlExecutorRequestDto,
    db: Session
) -> SqlExecutorResponseDto:
    target_schema = "ohdsi_test"
    user_sql = sqlExecutorRequestDto.sql
    
    pre_sql_filter_complete_timestamp = None
    post_sql_filter_complete_timestamp = None
    
    sqlExecutorResponseDto = None
    
    sql_execution_start_timestamp = None
    sql_execution_end_timestamp = None
    
    try:
        sql_execution_start_timestamp = datetime.now()
        db.execute(text(f"SET search_path TO {target_schema}, public;"))
        sql_execution_end_timestamp = datetime.now()
        
        result = db.execute(text(user_sql))
        if result.returns_rows:
            rows = result.fetchall()
            processed_data = [dict(row._mapping) for row in rows]
            
            sqlExecutorResponseDto = SqlExecutorResponseDto(data=processed_data, error=None)
            return sqlExecutorResponseDto
        else:
            db.commit()
            sqlExecutorResponseDto = SqlExecutorResponseDto(
                data={"message": "Query executed successfully.", "rowcount": result.rowcount},
                error=None
            )
            return sqlExecutorResponseDto

    except SQLAlchemyError as db_err:
        db.rollback()
        print(f"Database Error: {db_err}")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="An error occurred while executing the SQL query.")

    except Exception as e:
        db.rollback()
        print(f"Unexpected Error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")

    finally:
        save_sql_executor_log(
            SqlExecutorLogRequestModel(
                sql = sqlExecutorRequestDto.sql,
                # sql_validation_reason = 
                
                pre_sql_filter_complete_timestamp = pre_sql_filter_complete_timestamp,
                post_sql_filter_complete_timestamp = post_sql_filter_complete_timestamp,
                
                # sql_execution_status =
                sql_error_message = sqlExecutorResponseDto.error,
                
                result_row_count = result.rowcount,
                
                sql_execution_start_timestamp =sql_execution_start_timestamp,
                sql_execution_end_timestamp = sql_execution_end_timestamp
            )
        )