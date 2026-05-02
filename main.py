from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(title="Library REST API")

app.include_router(router)