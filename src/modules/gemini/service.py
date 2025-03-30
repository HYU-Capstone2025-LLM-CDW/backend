from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from src.config import settings
from src.modules.sql_generator.dto import SqlGeneratorRequestDto

_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_output_tokens=200,
    google_api_key=settings.gemini_api_key
)

def generate_response(prompt: str, textToSQLRequest: SqlGeneratorRequestDto) -> str:
    chain = PromptTemplate.from_template(prompt) | _llm
    return chain.invoke(textToSQLRequest.model_dump())
