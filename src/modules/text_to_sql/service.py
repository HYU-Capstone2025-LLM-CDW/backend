from functools import lru_cache
from src.modules.text_to_sql.dto import TextToSQLRequestDto, TextToSQLResponseDto
from src.modules.text_to_sql.rag import retrieve_relevant_query
from src.modules.gemini import service as gemini_service
from langchain_community.document_loaders import UnstructuredMarkdownLoader

@lru_cache()
def _get_prompt() -> str:
    loader = UnstructuredMarkdownLoader("src/modules/text_to_sql/prompt.md")
    data = loader.load()
    
    # print(data)
    return data[0].page_content
    
def convert_text_to_sql(textToSqlRequestDto: TextToSQLRequestDto) -> TextToSQLResponseDto:
    # prompt 생성 및 SQL_EXAMPLE을 불러옴
    prompt = _get_prompt()
    examples = retrieve_relevant_query(textToSqlRequestDto.text)
    
    # prompt 에 추가
    prompt.join("\n Here are Few Examples\n")
    prompt.join(examples)
    
    return gemini_service.generate_response(prompt, textToSqlRequestDto)