import faiss
import numpy as np
import os
import logging

from src.modules.sql_generator.dto import SqlGeneratorRequestDto, SqlGeneratorResponseDto
from src.modules.gemini import service as gemini_service
from sentence_transformers import SentenceTransformer
from src.modules.omop import service as omop_service
    
def generate(sqlGeneratorRequestDto: SqlGeneratorRequestDto) -> SqlGeneratorResponseDto:
    model_service = gemini_service
    prompt = omop_service.get_prompt()
    
    #RAG를 사용한 Example 을 반영하는 코드
    example = None # _add_relevant_query(sqlGeneratorRequestDto.text)
    
    # Example 이 존재할 때만 예시 추가
    if example:
        prompt += "\n There are some few examples \n"
        prompt += "\n".join(example)
        prompt += "\n Please answer the questions based on the reference documents above."

    result = model_service.generate_response(prompt, sqlGeneratorRequestDto)
    content = result.content
    
    sqlGeneratorResponseDto = SqlGeneratorResponseDto(
        sql=content.get("sql"),
        error=content.get("error")
    )
    
    # LOG 저장
    log_sql_generator(sqlGeneratorRequestDto, sqlGeneratorResponseDto)
    
    return sqlGeneratorResponseDto

""" RAG(Retrieval-Augmented Generation) """ 

# 임베딩 모델 로드, 영어 지원
_embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# 추후 search_history(LOG), data set 등 에서 불러오는 작업 필요
_query_list = ["Make SQL person group by race"]
_sql_list = ["SELECT race_concept_id, COUNT(*) AS person_count FROM person GROUP BY race_concept_id"]

# Vector DB(_query_index) 생성, 현재는 서버를 실행할 때 생성함
_query_index = faiss.IndexFlatL2(_embedding_model.get_sentence_embedding_dimension())

# _query_list 를 vector 화 시켜서  vector DB 에 추가
_query_index.add(np.array(_embedding_model.encode(_query_list)))

# Query 와 유사했던 이전의 Query 와 그에 대한 SQL을 Example 로 보내는 함수, top_k개의 example 선정
# sql_generator 의 service.py 에서만 실행하므로 private 함수로 설정
def _add_relevant_query(query: str, top_k: int = 1) -> list[str]:
    
    # 사용자의 Query 를 Vector 화 후 Vector DB 에서 비슷하다고 판단되는 Query의 index 를 찾고 반환
    query_vector = _embedding_model.encode([query])
    distances, indices = _query_index.search(query_vector, top_k)
    
    # 현재는 유사하다고 판단되는 example 을 top_k 만큼 보내는 형식
    # 유사한 정도인 distance 는 사용하지 않고 있으나 추후 최소치 같은 방법으로 사용할 수도 있음.
    return [(f"query : {_query_list[i]}, sql : {_sql_list[i]}") for i in indices[0]]
