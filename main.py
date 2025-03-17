from fastapi import FastAPI
from src.modules.text_to_sql.router import router as text_to_sql_router

app = FastAPI()

app.include_router(text_to_sql_router)
