import re
from sqlalchemy import inspect
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import SQLAlchemyError

# LLM에 의해 변환된 SQL문에 대한 검증을 담당합니다.

def contains_dml_statements(sql: str) -> bool:
    """
    변환된 SQL 쿼리에 데이터 변경(DML) 명령어가 포함되어 있는지 확인
    """
    dml_pattern = r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE)\b"
    return re.search(dml_pattern, sql, re.IGNORECASE) is not None


def check_table_and_column_validity(sql: str, engine: Engine) -> dict:
    """
    SQL 쿼리에 존재하지 않는 테이블이나 컬럼이 사용되었는지 검사

    반환값 예시:
    {
        "valid": False,
        "missing_tables": ["nonexistent_table"],
        "missing_columns": ["patients.nonexistent_column"]
    }
    """
    result = {
        "valid": True,
        "missing_tables": [],
        "missing_columns": []
    }

    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        # 테이블명 검사
        tables_in_query = []
        for word in sql.split():
            if word.upper() in ["FROM", "JOIN"]:
                table = sql.split(word)[1].strip().split()[0]
                tables_in_query.append(table)

        for table in tables_in_query:
            if table not in existing_tables:
                result["valid"] = False
                result["missing_tables"].append(table)

        # 컬럼 검사
        table_columns_map = {
            table: [col["name"].lower() for col in inspector.get_columns(table)]
            for table in existing_tables
        }

        matches = re.findall(r"(\w+)\.(\w+)", sql)  # ex) patients.age
        for table, column in matches:
            if table not in table_columns_map:
                continue  # 이미 missing_tables로 체크됨
            if column.lower() not in table_columns_map[table]:
                result["valid"] = False
                result["missing_columns"].append(f"{table}.{column}")

    except SQLAlchemyError as e:
        result["valid"] = False
        result["error"] = str(e)

    return result
