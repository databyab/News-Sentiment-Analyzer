from fastapi import FastAPI
from pydantic import BaseModel

from backend.sentiment_model import predict_sentiment
from backend.topic_analyzer import analyze_topic

app = FastAPI()


class TextRequest(BaseModel):
    text: str


class TopicRequest(BaseModel):
    topic: str


@app.get("/")
def home():
    return {"message": "Sentiment Intelligence API running"}


@app.post("/predict")
def analyze_sentiment(request: TextRequest):

    result = predict_sentiment(request.text)

    return result


@app.post("/analyze-topic")
def analyze_topic_endpoint(request: TopicRequest):

    # temporary tweets (later replaced with Twitter API)
    sample_tweets = [
        f"{request.topic} cars are amazing",
        f"{request.topic} autopilot is dangerous",
        f"{request.topic} stock is doing great",
        f"{request.topic} battery issues reported"
    ]

    result = analyze_topic(sample_tweets)

    return result