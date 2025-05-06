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
    
    # LOG 기록 용도 변수, __init__ 에 들어가지 않는다.
    input_received_timestamp: datetime = Field(
        None,
        description="input received timestamp",
        init=False,
        exclude=True
    )
    pre_llm_filter_status : Optional[str] = Field(None, description="Text filtering result ('passed', 'rejected')", init=False, exclude=True)
    pre_llm_filter_reason : Optional[str] = Field(None, description="Text filtering reason", init=False, exclude=True)
    
    pre_llm_filter_complete_timestamp : datetime = Field(
        None,
        description="Text filtering completed timestamp",
        init=False,
        exclude=True
    )
    
    # LOG 에 기록 위해서 코드 구조 변경
    # 기존 코드는 dto 내부 변수 변경 불가
    @model_validator(mode='after')
    def validate_text(self):
        # 필터링 상태 초기화 (혹시 모를 경우 대비, init=False로 인해 초기값은 None임)
        self.pre_llm_filter_status = 'passed' # 기본값 'passed'로 시작
        self.pre_llm_filter_reason = None
        self.input_received_timestamp = datetime.now()

        try:
            # 정의한 validator 클래스들을 사용하여 검증 수행
            BasicTextValidator(self.text).validate()
            SecureTextValidator(self.text).validate()

            # 모든 validator를 통과하면 상태는 'passed'로 유지됨
            
        except Exception as e:
            # 예상치 못한 다른 예외 발생 시
            self.pre_llm_filter_status = 'rejected'
            self.pre_llm_filter_reason = f"Unexpected validation error: {type(e).__name__} - {str(e)}"
            
            # 오류 사항 로그
            save_sql_generator_log(LogSqlGeneratorRequestModel(
                user_input_text = self.text,
                input_received_timestamp = self.input_received_timestamp,
                
                pre_llm_filter_status = self.pre_llm_filter_status,
                pre_llm_filter_reason = self.pre_llm_filter_reason,

                llm_model_used = "GEMINI")
            )
            
            raise HTTPException(status_code=400, detail=str(e))

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