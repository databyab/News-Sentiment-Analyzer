from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.news_fetcher import fetch_news
from backend.services.sentiment_analyzer import analyze_topic

router = APIRouter()

class TopicRequest(BaseModel):
    topic: str


@router.post("/analyze-topic")
def analyze_topic_endpoint(request: TopicRequest):

    news = fetch_news(request.topic)

    result = analyze_topic(news)

    return result