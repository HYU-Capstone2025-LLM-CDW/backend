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
                _apply_masking(dict(row._mapping), idx + 1) 
                for idx, row in enumerate(rows)
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
    
"""
    Data Masking Code
    
    기본 str : ~~~ + index 
    lamda : lamda 에서 지정한 대로, index 안 붙음
""" 

_MASKING_RULES = {
    "person_id" : "임시사람id_",
    "gender_concept_id" : lambda g : "마스킹",
    "race_concept_id" : lambda g : "마스킹",
}

def _apply_masking(row_dict : dict , row_index : int) -> dict:
    masked = {}
    for key, value in row_dict.items():
        if key in _MASKING_RULES:
            rule = _MASKING_RULES[key]
            
            # rule 이 함수 일시, 함수에 따름
            if callable(rule):
                masked[key] = rule(value)
                
            # rule 이 그냥 str 등일시 rule + index 로 masking
            else:
                masked[key] = f"{rule}{row_index}"
        else:
            masked[key] = value
    return masked