from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException

from src.modules.log.dto import SqlGeneratorLogRequestModel
from src.config import settings
from src.database import get_db_internal

import traceback


def save_sql_generator_log (db_log : SqlGeneratorLogRequestModel):
    db = get_db_internal()
    
    try:    
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log
    
    except SQLAlchemyError as db_err:
        db.rollback()
        print(f"Database Error: {db_err}")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="An error occurred while saving sql_generator_log.")

    except Exception as e:
        db.rollback()
        print(f"Unexpected Error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="An unexpected server error occurred.")
    
    finally:
        db.close()