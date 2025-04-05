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
    
    result = model_service.generate_response(_get_prompt(), sqlGeneratorRequestDto)
    content = result.content
    
    return SqlGeneratorResponseDto(
        sql=content.get("sql"),
        error=content.get("error")
    )

## RAG

# 임베딩 모델 로드, 영어 지원
_embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# 추후 search_history(LOG), data set 등 에서 불러오는 작업 필요
_query_list = ["Make SQL person group by race"]
_sql_list = ["SELECT race_concept_id, COUNT(*) AS person_count FROM person GROUP BY race_concept_id"]


# Vector DB 생성
_query_index = faiss.IndexFlatL2(_embedding_model.get_sentence_embedding_dimension())
_query_vectors = _embedding_model.encode(_query_list)
_query_index.add(np.array(_query_vectors))

# Query 와 유사했던 이전의 Query 를 찾고 그에 대한 SQL을 Example 로 보내는 함수, 현재는 3개의 example 선정 중
def retrieve_relevant_query(query: str, top_k: int = 3) -> list:
    query_vector = _embedding_model.encode([query])
    distances, indices = _query_index.search(query_vector, top_k)
    
    return [_sql_list[i] for i in indices[0]]