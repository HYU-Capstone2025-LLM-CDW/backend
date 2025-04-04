from fastapi import FastAPI
from src.modules.sql_generator.router import router as sql_generator_router
from src.modules.sql_executor.router import router as sql_executor_router

app = FastAPI()

app.include_router(sql_generator_router)
app.include_router(sql_executor_router)

@app.get("/", response_model=dict, tags=["Health Check"])
def health_check():
    return {"status": "ok"}