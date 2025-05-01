from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.modules.log.dto import LogSqlGeneratorRequestModel, base
from src.config import settings

# PostgreSQL 연결 설정
_database_url = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
_engine = create_engine(_database_url)

_session_local = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


# log table 없을 시 생성
def create_sql_generator_table():
    base.metadata.create_all(_engine)

create_sql_generator_table()

def save_sql_generator_log (db_log : LogSqlGeneratorRequestModel):
    db = _session_local()
    
    try:    
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log
    
    except Exception as e:
        print(e)
    
    finally:
        db.close()