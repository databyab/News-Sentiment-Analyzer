from fastapi import HTTPException

from backend.models.sentiment_model import predict_sentiment
from backend.services.analytics import sentiment_distribution, extract_keywords

MAX_INPUT_ITEMS = 20


def analyze_topic(texts):
    if not texts:
        raise HTTPException(status_code=404, detail="No news articles were found for this topic.")

    if len(texts) > MAX_INPUT_ITEMS:
        texts = texts[:MAX_INPUT_ITEMS]

    results = []

    for text in texts:

        sentiment = predict_sentiment(text)

        results.append(sentiment)

    distribution = sentiment_distribution(results)

    keywords = extract_keywords(texts)

    return {
        "results": results,
        "sentiment_distribution": distribution,
        "keywords": keywords
    }


if __name__ == "__main__":

    sample_tweets = [
        "Tesla cars are amazing",
        "Tesla autopilot is dangerous",
        "Tesla stock is doing great",
        "Tesla battery issues reported"
    ]

    data = analyze_topic(sample_tweets)

    print(data)
