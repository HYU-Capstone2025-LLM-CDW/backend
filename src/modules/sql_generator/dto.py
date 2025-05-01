from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime

from src.validator.text_validator.basic_text_validator import BasicTextValidator
from src.validator.text_validator.secure_text_validator import SecureTextValidator
from src.validator.sql_validator.basic_sql_validator import BasicSQLValidator

from src.modules.log.dto import LogSqlGeneratorRequestModel
from src.modules.log.service import save_sql_generator_log

class SqlGeneratorRequestDto(BaseModel):
    text: str = Field(..., title="Text to convert to SQL", description="The text to convert to SQL")
    
    input_received_timestamp: datetime = Field(
        
        # 이것은 datetime.now 로 해주어야 함, datatime.now() 시 오류류
        default_factory= datetime.now,
        description="input received timestamp",
        init=False
    )
    pre_llm_filter_status : Optional[str] = Field(None, description="LLM 호출 전 텍스트 필터링 결과 ('passed', 'rejected')", init=False)
    pre_llm_filter_reason : Optional[str] = Field(None, description="텍스트 필터링에서 거부된 이유 (e.g., 'profanity_detected', 'rule_id: [ID]')", init=False)
    
    pre_llm_filter_complete_timestamp : datetime = Field(
        None,
        description="텍스트 필터링 완료 시간",
        init=False
    )
    
    @model_validator(mode='after')
    def apply_llm_filters(self):
        # 필터링 상태 초기화 (혹시 모를 경우 대비, init=False로 인해 초기값은 None임)
        self.pre_llm_filter_status = 'passed' # 기본값 'passed'로 시작
        self.pre_llm_filter_reason = None

        try:
            # 정의한 validator 클래스들을 사용하여 검증 수행
            BasicTextValidator(self.text).validate()
            SecureTextValidator(self.text).validate()

            # 모든 validator를 통과하면 상태는 'passed'로 유지됨
            
        except Exception as e:
            # 예상치 못한 다른 예외 발생 시
            self.pre_llm_filter_status = 'rejected'
            self.pre_llm_filter_reason = f"Unexpected validation error: {type(e).__name__} - {str(e)}"
            
            
            save_sql_generator_log(LogSqlGeneratorRequestModel(
            user_input_text = self.text,
            input_received_timestamp = self.input_received_timestamp,
            
            pre_llm_filter_status = self.pre_llm_filter_status,
            pre_llm_filter_reason = self.pre_llm_filter_reason,

            llm_model_used = "GEMINI"
            
        ))
            
            raise HTTPException(status_code=400, detail=str(e))
            # 필요에 따라 로깅 또는 에러 처리 추가

        self.pre_llm_filter_complete_timestamp = datetime.now()
        return self
    
    # @field_validator("text")
    # def validate_text(cls, value):
    #     try:
    #         BasicTextValidator(value).validate()
    #         SecureTextValidator(value).validate()
            
    #     except Exception as e:
    #         raise HTTPException(status_code=400, detail=str(e))
        
    #     return value
    
class SqlGeneratorResponseDto(BaseModel):
    sql: Optional[str] = Field(None, title="SQL", description="The generated SQL")
    error: Optional[str] = Field(None, title="Error", description="The error message if an error occurred")