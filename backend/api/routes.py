from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.services.news_fetcher import fetch_news
from backend.services.sentiment_analyzer import analyze_topic

router = APIRouter()


class TopicRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=100)


class SentimentResult(BaseModel):
    text: str
    sentiment: str
    confidence: float


class AnalysisResponse(BaseModel):
    results: List[SentimentResult]
    sentiment_distribution: dict[str, float]
    keywords: List[str]


@router.post("/analyze-topic", response_model=AnalysisResponse)
def analyze_topic_endpoint(request: TopicRequest):
    news = fetch_news(request.topic)
    result = analyze_topic(news)
    return result
