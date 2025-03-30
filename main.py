from fastapi import FastAPI
from src.modules.sql_generator.router import router as sql_generator_router

app = FastAPI()

app.include_router(sql_generator_router)
