from sqlglot import parse_one, exp

# 필요시 추가 및 수정 필요
SENSITIVE_COLUMNS = {"person_id", "location_id", "provider_id", "care_site_id"}

class SQLSecurityValidator:
    """
    SQLSecurityValidator 클래스는 생성된 SQL 쿼리가 민감한 정보(컬럼)에 접근하는지를 검증합니다.

    주요 검증 항목:
    1. 민감 컬럼(person_id, location_id 등)에 대한 SELECT 접근 차단

    메서드:
    - __init__(self, sql: str): SQL 문자열을 파싱하여 AST를 생성
    - validate(self): 전체 보안 검증 실행
    - _block_sensitive_columns(self): 민감 컬럼 접근 여부 검증
    """

    def __init__(self, sql: str):
        self.sql = sql
        self.ast = parse_one(sql, read="postgres")

    def validate(self):
        """
        SQL 쿼리의 보안 위험 요소를 검증하는 메서드입니다.

        Raises:
            ValueError: 민감 정보 컬럼에 접근한 경우 발생합니다.
        """
        self._block_sensitive_columns()

    def _block_sensitive_columns(self):
        """
        SQL AST 내 사용된 컬럼 중 민감한 컬럼이 포함되어 있는지 확인합니다.

        Raises:
            ValueError: 사용된 컬럼 중 민감 컬럼이 포함된 경우
        """
        used_columns = set()
        for col in self.ast.find_all(exp.Column):
            used_columns.add(col.name.lower())

        accessed_sensitive = used_columns & SENSITIVE_COLUMNS
        if accessed_sensitive:
            raise ValueError(f"민감정보 접근이 허용되지 않습니다: {', '.join(accessed_sensitive)}")
