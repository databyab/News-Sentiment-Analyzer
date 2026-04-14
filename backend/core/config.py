import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_TIMEOUT_SECONDS = int(os.getenv("NEWS_API_TIMEOUT_SECONDS", "10"))
STREAMLIT_BACKEND_URL = os.getenv("STREAMLIT_BACKEND_URL", "http://127.0.0.1:8000")
