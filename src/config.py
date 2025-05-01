from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    gemini_api_key: str
    cors_origins: list[str] = ["*"]
    db_name: str
    db_user: str
    db_password: str
    db_host : str
    db_port : str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    
settings = _Settings()