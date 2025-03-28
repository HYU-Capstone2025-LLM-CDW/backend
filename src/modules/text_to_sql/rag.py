import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# 임베딩 모델 로드, 한글을 더 잘 지원해주는 임베딩 모델을 사용해야 할 필요성이 있다.
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# search_history 에서 불러오는 작업 필요
QUERY_LIST = ["Make SQL person group by race"]
SQL_LIST = ["SELECT race_concept_id, COUNT(*) AS person_count FROM person GROUP BY race_concept_id"]


# Vector DB 생성
query_index = faiss.IndexFlatL2(embedding_model.get_sentence_embedding_dimension())
query_vectors = embedding_model.encode(QUERY_LIST)
query_index.add(np.array(query_vectors))

# Query 와 유사했던 이전의 Query 를 찾고 그에 대한 SQL을 Example 로 보내는 함수
def retrieve_relevant_query(query: str, top_k: int = 3) -> list:
    query_vector = embedding_model.encode([query])
    distances, indices = query_index.search(query_vector, top_k)
    
    return [SQL_LIST[i] for i in indices[0]]