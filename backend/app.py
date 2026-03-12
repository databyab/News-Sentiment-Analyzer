from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(title="News Sentiment Intelligence Platform")

app.include_router(router)