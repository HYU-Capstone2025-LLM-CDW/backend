from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from src.config import settings
from src.modules.text_to_sql.dto import TextToSQLRequestDto

from sqlalchemy import create_engine
from src.validator.sql_query_validator import (
    contains_dml_statements,
    check_table_and_column_validity
)

# DB 연결 (config.py의 settings에 database_url이 정의해야함)
engine = create_engine(settings.database_url)

_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_output_tokens=200,
    google_api_key=settings.gemini_api_key
)

def generate_response(prompt: str, textToSQLRequest: TextToSQLRequestDto) -> str:
    chain = PromptTemplate.from_template(prompt) | _llm
    sql = chain.invoke(textToSQLRequest.model_dump())

    # 변환된 sql문에 대해 유효성 검사 시작
    if contains_dml_statements(sql):
        raise ValueError("변환된 SQL에 데이터 변경 명령어가 포함되어 있습니다.")

    validation = check_table_and_column_validity(sql, engine)
    if not validation["valid"]:
        raise ValueError(f"잘못된 SQL입니다. 문제: {validation}")

    return sql
