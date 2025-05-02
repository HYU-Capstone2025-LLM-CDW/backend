from sqlglot import parse_one, exp

class SQLComplexityLimiter:
    """
    SQLComplexityLimiter 클래스는 생성한 SQL 쿼리의 복잡도를 제한하는 클래스입니다.

    주요 검증 항목:
    1. LIMIT 없는 SELECT 차단
    2. JOIN 개수 제한(최대 2개 이하)
    
    메서드:
    - __init__(self, sql: str): SQL 파싱 및 AST 생성
    - validate(self): 전체 복잡도 검증 실행
    - _require_limit_clause(self): LIMIT 절 존재 여부 확인
    - _limit_join_count(self, max_joins: int): JOIN 개수 제한
    """

    def __init__(self, sql: str):
        self.sql = sql
        self.ast = parse_one(sql, read="postgres")

    def validate(self):
        """
        LLM이 변환한 SQL 쿼리의 복잡도를 검증하는 메서드입니다.

        이 메서드는 쿼리에서 LIMIT 절 누락 여부와 JOIN 개수를 검사합니다.

        Raises:
            ValueError: 복잡도 제약 조건을 위반한 경우 발생합니다.
        """
        self._require_limit_clause()
        self._limit_join_count(max_joins=2)

    def _require_limit_clause(self):
        """
        LIMIT 절이 포함되어 있는지 확인하는 메서드입니다.

        모든 SELECT 문을 대상으로 LIMIT 존재 여부를 검사합니다.

        Raises:
            ValueError: LIMIT 절이 없는 SELECT 문이 발견될 경우 발생합니다.
        """
        for select in self.ast.find_all(exp.Select):
            if not select.args.get("limit"):
                raise ValueError("SELECT 문에는 반드시 LIMIT 절이 포함되어야 합니다.")

    def _limit_join_count(self, max_joins: int):
        """
        SQL 쿼리 내 JOIN 개수가 허용된 최대치를 초과하지 않았는지 확인하는 메서드입니다.

        Args:
            max_joins (int): 허용할 최대 JOIN 개수

        Raises:
            ValueError: JOIN 개수가 제한을 초과한 경우 발생합니다.
        """
        join_count = sum(1 for _ in self.ast.find_all(exp.Join))
        if join_count > max_joins:
            raise ValueError(f"JOIN 개수가 너무 많습니다. 최대 허용: {max_joins}, 현재: {join_count}")
