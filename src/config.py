import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class _Settings(BaseSettings):
    gemini_api_key: str = ""
    cors_origins: list[str] = ["*"]
    
    postgres_user: str
    postgres_password: str
    postgres_db: str
    
    database_url: str = ""
    db_host: str
    db_port: int
    
    log_db_name: str
    log_db_user: str
    log_db_password: str
    log_db_host : str
    log_db_port : str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    
settings = _Settings()