import requests
from fastapi import HTTPException

from backend.core.config import NEWS_API_KEY, NEWS_API_TIMEOUT_SECONDS

URL = "https://newsapi.org/v2/everything"
MAX_TOPIC_LENGTH = 100
MAX_ARTICLES = 20


def fetch_news(topic, limit=20):
    normalized_topic = (topic or "").strip()
    if not normalized_topic:
        raise HTTPException(status_code=400, detail="Topic is required.")

    if len(normalized_topic) > MAX_TOPIC_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Topic must be at most {MAX_TOPIC_LENGTH} characters long.",
        )

    if not NEWS_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: NEWS_API_KEY is missing.",
        )

    safe_limit = max(1, min(int(limit), MAX_ARTICLES))

    params = {
        "q": normalized_topic,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": safe_limit,
        "apiKey": NEWS_API_KEY,
    }

    try:
        response = requests.get(URL, params=params, timeout=NEWS_API_TIMEOUT_SECONDS)

        response.raise_for_status()

        data = response.json()

        articles = data.get("articles", [])

        headlines = []

        for article in articles:
            title = article.get("title")
            if title:
                cleaned_title = title.strip()
                if cleaned_title:
                    headlines.append(cleaned_title[:300])

        return headlines

    except requests.exceptions.Timeout as exc:
        raise HTTPException(
            status_code=504,
            detail="Timed out while contacting the news provider.",
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch news from the upstream provider.",
        ) from exc
