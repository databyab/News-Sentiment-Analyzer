import requests
from backend.core.config import NEWS_API_KEY

URL = "https://newsapi.org/v2/everything"


def fetch_news(topic, limit=20):

    params = {
        "q": topic,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": limit,
        "apiKey": NEWS_API_KEY
    }

    try:
        response = requests.get(URL, params=params)

        response.raise_for_status()

        data = response.json()

        articles = data.get("articles", [])

        headlines = []

        for article in articles:
            title = article.get("title")
            if title:
                headlines.append(title)

        return headlines

    except requests.exceptions.RequestException as e:

        print("News API request failed:", e)

        return []