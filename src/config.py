import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class _Settings(BaseSettings):
    gemini_api_key: str = ""
    cors_origins: list[str] = ["*"]
    
    postgres_user: str
    postgres_password: str
    postgres_db: str
    
    postgres_db_url: str = ""
    postgres_db_host: str
    postgres_db_port: int

    mssql_db_host: str
    mssql_db_user: str
    mssql_db_password: str
    mssql_db: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    
settings = _Settings()