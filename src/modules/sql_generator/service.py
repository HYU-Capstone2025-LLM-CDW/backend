from functools import lru_cache
from pprint import pprint
from src.modules.sql_generator.dto import SqlGeneratorRequestDto, SqlGeneratorResponseDto
from src.modules.gemini import service as gemini_service
from langchain_community.document_loaders import UnstructuredMarkdownLoader

# @lru_cache()
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
    