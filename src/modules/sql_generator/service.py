import faiss
import numpy as np
from functools import lru_cache
from src.modules.sql_generator.dto import SqlGeneratorRequestDto, SqlGeneratorResponseDto
from src.modules.gemini import service as gemini_service
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from sentence_transformers import SentenceTransformer
@lru_cache()
def _get_prompt() -> str:
    loader = UnstructuredMarkdownLoader("src/modules/sql_generator/prompt.md")
    data = loader.load()
    
    return data[0].page_content
    
def generate(sqlGeneratorRequestDto: SqlGeneratorRequestDto) -> SqlGeneratorResponseDto:
    model_service = gemini_service
    
    #RAG를 사용한 Example 을 반영하는 코드
    prompt = _get_prompt()
    prompt += "\n 아래 몇 개의 예시가 있습니다. \n"
    prompt += "\n".join(_add_relevant_query(sqlGeneratorRequestDto.text))
    
    result = model_service.generate_response(prompt, sqlGeneratorRequestDto)
    content = result.content
    
    return SqlGeneratorResponseDto(
        sql=content.get("sql"),
        error=content.get("error")
    )

""" RAG """ 

# 임베딩 모델 로드, 영어 지원
_embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# 추후 search_history(LOG), data set 등 에서 불러오는 작업 필요
_query_list = ["Make SQL person group by race"]
_sql_list = ["SELECT race_concept_id, COUNT(*) AS person_count FROM person GROUP BY race_concept_id"]

# Vector DB 생성, 현재는 서버를 실행할 때 생성함
_query_index = faiss.IndexFlatL2(_embedding_model.get_sentence_embedding_dimension())
_query_index.add(np.array(_embedding_model.encode(_query_list)))

# Query 와 유사했던 이전의 Query 와 그에 대한 SQL을 Example 로 보내는 함수, top_k개의 example 선정
# sql_generator 의 service.py 에서만 실행하므로 private 함수로 설정
def _add_relevant_query(query: str, top_k: int = 1) -> list[str]:
    query_vector = _embedding_model.encode([query])
    distances, indices = _query_index.search(query_vector, top_k)
    
    return [(f"query : {_query_list[i]}, sql : {_sql_list[i]}") for i in indices[0]]