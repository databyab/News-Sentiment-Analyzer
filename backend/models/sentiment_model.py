from transformers import pipeline

sentiment_model = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)

label_map = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive"
}

def predict_sentiment(text):
    safe_text = (text or "").strip()[:300]
    if not safe_text:
        return {
            "text": "",
            "sentiment": "neutral",
            "confidence": 0.0
        }

    result = sentiment_model(safe_text)[0]

    sentiment = label_map[result["label"]]
    confidence = result["score"]

    return {
        "text": safe_text,
        "sentiment": sentiment,
        "confidence": confidence
    }


if __name__ == "__main__":

    text = "Tesla cars are amazing"

    print(predict_sentiment(text))
