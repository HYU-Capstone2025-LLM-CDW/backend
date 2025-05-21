import pymssql
from src.config import settings
from typing import List, Dict, Any

def _get_connection():
    try:
        return pymssql.connect(
            host=settings.mssql_db_host,
            user=settings.mssql_db_user,
            password=settings.mssql_db_password,
            database=settings.mssql_db,
        )
    except pymssql.Error as e:
        print(e)
        raise

def get_omop_data(query: str) -> List[Dict[str, Any]]:
    conn = None
    cursor = None
    try:
        conn = _get_connection()
        cursor = conn.cursor(as_dict=True)  # 딕셔너리 형태로 결과 반환
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except pymssql.Error as e:
        print(e)
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
