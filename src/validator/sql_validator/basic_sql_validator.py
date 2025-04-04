from sqlglot import parse_one

class BasicSQLValidator:
    def __init__(self, sql: str):
        self.sql = sql
        
    def validate(self):
        try:
            self.ast = parse_one(self.sql, read="postgres")
        except Exception as e:
            raise ValueError(str(e))
        
    def _validate_allowed_tables(self):
        pass
    
    def _validate_allowed_columns(self):
        pass
    
    def _validate_allowed_dml(self):
        pass
    
    def _validate_allowed_ddl(self):
        pass
    
    def _validate_allowed_keywords(self):
        pass
    