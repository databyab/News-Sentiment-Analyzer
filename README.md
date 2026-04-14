# News Sentiment Analyzer

This project fetches recent headlines for a topic, runs sentiment analysis on them, and shows the results through a FastAPI backend plus a Streamlit UI.


## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file:

```env
NEWS_API_KEY=your_newsapi_key
STREAMLIT_BACKEND_URL=http://127.0.0.1:8000
NEWS_API_TIMEOUT_SECONDS=10
```

You can start from `.env.example`.

## Run the backend

```bash
uvicorn backend.app:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with a health check at `/health`.

## Run the Streamlit UI

```bash
streamlit run frontend/streamlit_app.py
```

## Security hardening included

- Topic input is length-limited and validated.
- External API calls use timeouts.
- Missing API keys fail safely.
- Upstream request failures return controlled API errors instead of raw exceptions.
- Empty-result cases are handled explicitly.
