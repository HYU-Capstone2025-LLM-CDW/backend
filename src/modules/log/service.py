from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from src.modules.log.dto import SqlGeneratorLogRequestModel, base
from src.config import settings

import traceback

# PostgreSQL 연결 설정
_database_url = f"postgresql://{settings.log_db_user}:{settings.log_db_password}@{settings.log_db_host}:{settings.log_db_port}/{settings.log_db_name}"
_engine = create_engine(_database_url)

_session_local = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


# log table 없을 시 생성
def create_sql_generator_table():
    base.metadata.create_all(_engine)

create_sql_generator_table()

def save_sql_generator_log (db_log : SqlGeneratorLogRequestModel):
    db = _session_local()
    
    try:    
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log
    
    except SQLAlchemyError as db_err:
        db.rollback()
        print(f"Database Error: {db_err}")
        traceback.print_exc()
        

    except Exception as e:
        db.rollback()
        print(f"Unexpected Error: {e}")
        traceback.print_exc()
    
    finally:
        db.close()
