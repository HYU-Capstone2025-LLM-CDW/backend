from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from src.modules.sql_executor.dto import SqlExecutorRequestDto, SqlExecutorResponseDto
import traceback

async def execute(
    sqlExecutorRequestDto: SqlExecutorRequestDto,
    db: Session
) -> SqlExecutorResponseDto:
    target_schema = "ohdsi_test"
    user_sql = sqlExecutorRequestDto.sql
    
    try:
        db.execute(text(f"SET search_path TO {target_schema}, public;"))

        result = db.execute(text(user_sql))
        if result.returns_rows:
            rows = result.fetchall()
            processed_data = [
                apply_masking(dict(row._mapping)) 
                for row in rows
            ]
            return SqlExecutorResponseDto(data=processed_data, error=None)
        else:
            db.commit()
            return SqlExecutorResponseDto(
                data={"message": "Query executed successfully.", "rowcount": result.rowcount},
                error=None
            )

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
    
    

_MASKING_RULES = {
    "person_id" : "임시사람id",
    "gender_concept_id" : "임시성별id",
    "race_concept_id" : "임시인종id"
}

def apply_masking(row_dict):
    masked = {}
    for key, value in row_dict.items():
        if key in _MASKING_RULES:
            rule = _MASKING_RULES[key]
            if callable(rule):
                masked[key] = rule(value)
            else:
                masked[key] = f"{rule}"
        else:
            masked[key] = value
    return masked