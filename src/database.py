# app/database.py 파일

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy 엔진 생성
# connect_args는 필요에 따라 추가 (예: SSL 설정)
_engine = create_engine(os.getenv("DATABASE_URL")) # .env에서 로드한 URL 사용

# 데이터베이스 세션 생성기
_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

# 모든 모델이 상속할 기본 클래스
# 이 Base 객체가 Alembic과 모델을 연결하는 핵심입니다.
Base = declarative_base()

# FastAPI 의존성 주입용 함수 (요청마다 세션 생성 및 반환)
def get_db():
    db = _SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Error in database session: {e}")
        db.rollback()
        raise
    finally:
        db.close()