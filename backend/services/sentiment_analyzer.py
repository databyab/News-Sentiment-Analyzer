from backend.models.sentiment_model import predict_sentiment
from backend.services.analytics import sentiment_distribution, extract_keywords

def analyze_topic(tweets):

    results = []

    for tweet in tweets:

        sentiment = predict_sentiment(tweet)

        results.append(sentiment)

    distribution = sentiment_distribution(results)

    keywords = extract_keywords(tweets)

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