from functools import lru_cache
from src.modules.text_to_sql.dto import TextToSQLRequestDto, TextToSQLResponseDto
from src.modules.gemini import service as gemini_service
from langchain_community.document_loaders import UnstructuredMarkdownLoader

@lru_cache()
def _get_prompt() -> str:
    loader = UnstructuredMarkdownLoader("src/modules/text_to_sql/prompt.md")
    data = loader.load()
    
    # print(data)
    return data[0].page_content
    
def convert_text_to_sql(textToSqlRequestDto: TextToSQLRequestDto) -> TextToSQLResponseDto:
    return gemini_service.generate_response(_get_prompt(), textToSqlRequestDto)