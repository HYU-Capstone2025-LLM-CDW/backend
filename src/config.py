from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    gemini_api_key: str
    cors_origins: list[str] = ["*"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    
settings = _Settings()