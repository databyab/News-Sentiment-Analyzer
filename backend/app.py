from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(title="News Sentiment Intelligence Platform")


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


app.include_router(router)
