from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# sqlAlchemy Model 정의
base = declarative_base()

class LogSqlGeneratorRequestModel(base):
    
    __tablename__ = "sql_generator_log"
    
    log_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    # session_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    input_received_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=True, server_default=func.now())
    user_input_text: Mapped[str] = mapped_column(Text, nullable=True)
    
    pre_llm_filter_status: Mapped[str] = mapped_column(String(50), nullable=True)
    pre_llm_filter_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    pre_llm_filter_complete_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    generated_sql: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    llm_request_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    llm_response_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    sql_validation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    llm_model_used: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    