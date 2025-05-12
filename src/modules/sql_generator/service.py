import faiss
import numpy as np
import os
import logging
import traceback

from datetime import datetime
from src.modules.sql_generator.dto import SqlGeneratorRequestDto, SqlGeneratorResponseDto
from src.modules.gemini import service as gemini_service
from sentence_transformers import SentenceTransformer
from src.modules.omop import service as omop_service

from src.modules.log.dto import SqlGeneratorLogRequestModel
from src.modules.log.service import save_sql_generator_log
from fastapi import HTTPException


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

        llm_request_timestamp = datetime.now()
        result = model_service.generate_response(prompt, sqlGeneratorRequestDto)
        llm_response_timestamp = datetime.now()
        
        content = result.content
        
        sqlGeneratorResponseDto = SqlGeneratorResponseDto(
            sql=content.get("sql"),
            error=content.get("error")
        )
        
        save_sql_generator_log(SqlGeneratorLogRequestModel(
            user_input_text = sqlGeneratorRequestDto.text,
            input_received_timestamp = sqlGeneratorRequestDto.input_received_timestamp,
            
            pre_llm_filter_status = sqlGeneratorRequestDto.pre_llm_filter_status,
            pre_llm_filter_reason = sqlGeneratorRequestDto.pre_llm_filter_reason,
            pre_llm_filter_complete_timestamp = sqlGeneratorRequestDto.pre_llm_filter_complete_timestamp,
            
            generated_sql = sqlGeneratorResponseDto.sql,
            
            llm_request_timestamp = llm_request_timestamp,
            llm_response_timestamp = llm_response_timestamp,
            
            llm_validation_reason = sqlGeneratorResponseDto.error,
            
            llm_model_used = "GEMINI"
        ))
      
        return sqlGeneratorResponseDto

    except Exception as e:
        print(f"Unexpected Error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")


""" RAG(Retrieval-Augmented Generation) """ 

def _rag_init():
    # 임베딩 모델 로드, 영어 지원
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # file_names
    file_path = "src/modules/sql_generator/"
    query_file = "query_example.md"
    sql_file = "sql_example.md"
    index_file = "query_index.faiss"
    
    # 추후 search_history(LOG), data set 등 에서 불러오는 작업 필요
    query_list = []
    
    with open(file_path + query_file, 'r', encoding='utf-8') as file:
        for line in file:
            query_list.append(line.strip())
    
    
    sql_list = [] 
    with open(file_path + sql_file, 'r', encoding='utf-8') as file:
        content = file.read()
        
    sql_list = [q.strip() for q in content.split(';') if q.strip()]
    
    # Vector DB 불러오기 없을 시 새로 생성
    index_path = file_path + index_file
    if os.path.exists(index_path):
        query_index = faiss.read_index(index_path)
    
    # Vector DB(_query_index)
    else :
        query_index = faiss.IndexFlatL2(embedding_model.get_sentence_embedding_dimension())

        # _query_list 를 vector 화 시켜서  vector DB 에 추가
        query_index.add(np.array(embedding_model.encode(query_list)))
        faiss.write_index(query_index, index_path)
    
    
    return embedding_model, query_list, sql_list, query_index

# Query 와 유사했던 이전의 Query 와 그에 대한 SQL을 Example 로 보내는 함수, top_k개의 example 선정
# sql_generator 의 service.py 에서만 실행하므로 private 함수로 설정
def _add_relevant_query(query: str, top_k: int = 1) -> list[str]:
    
    if not _query_list or not _sql_list:
        return []
    
    # 사용자의 Query 를 Vector 화 후 Vector DB 에서 비슷하다고 판단되는 Query의 index 를 찾고 반환
    query_vector = _embedding_model.encode([query])
    distances, indices = _query_index.search(query_vector, top_k)
    
    # 현재는 유사하다고 판단되는 example 을 top_k 만큼 보내는 형식
    # 유사한 정도인 distance 는 사용하지 않고 있으나 추후 최소치 같은 방법으로 사용할 수도 있음.
    return [(f"query : {_query_list[i]}, sql : {_sql_list[i]}") for i in indices[0]]