import os

import pandas as pd
import requests
import streamlit as st


BACKEND_URL = os.getenv("STREAMLIT_BACKEND_URL", "http://127.0.0.1:8000")
ANALYZE_ENDPOINT = f"{BACKEND_URL.rstrip('/')}/analyze-topic"
REQUEST_TIMEOUT_SECONDS = 20


def analyze_topic(topic: str) -> dict:
    response = requests.post(
        ANALYZE_ENDPOINT,
        json={"topic": topic},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()


st.set_page_config(
    page_title="News Sentiment Analyzer",
    page_icon="N",
    layout="wide",
)

st.title("News Sentiment Analyzer")
st.caption("Explore recent headlines for a topic and see the model's sentiment breakdown.")

with st.form("topic-form"):
    topic = st.text_input("Topic", placeholder="Tesla, Apple, inflation, elections...")
    submitted = st.form_submit_button("Analyze")

if submitted:
    cleaned_topic = topic.strip()

    if not cleaned_topic:
        st.warning("Enter a topic to analyze.")
    else:
        with st.spinner("Fetching headlines and running sentiment analysis..."):
            try:
                payload = analyze_topic(cleaned_topic)
            except requests.HTTPError as exc:
                detail = "Request failed."
                try:
                    detail = exc.response.json().get("detail", detail)
                except ValueError:
                    pass
                st.error(detail)
            except requests.RequestException:
                st.error("Could not reach the backend API. Make sure FastAPI is running.")
            else:
                results_df = pd.DataFrame(payload["results"])
                distribution = payload["sentiment_distribution"]
                keywords = payload["keywords"]

                metric_columns = st.columns(3)
                metric_columns[0].metric("Articles analyzed", len(results_df))
                metric_columns[1].metric(
                    "Top sentiment",
                    max(distribution, key=distribution.get) if distribution else "n/a",
                )
                metric_columns[2].metric("Keywords found", len(keywords))

                left, right = st.columns([1, 2])

                with left:
                    st.subheader("Sentiment Distribution")
                    if distribution:
                        distribution_df = pd.DataFrame(
                            {
                                "sentiment": list(distribution.keys()),
                                "percentage": list(distribution.values()),
                            }
                        ).set_index("sentiment")
                        st.bar_chart(distribution_df)
                    else:
                        st.info("No sentiment distribution available.")

                    st.subheader("Keywords")
                    if keywords:
                        st.write(", ".join(keywords))
                    else:
                        st.info("No keywords extracted.")

                with right:
                    st.subheader("Headline-Level Results")
                    if not results_df.empty:
                        results_df["confidence"] = results_df["confidence"].map(
                            lambda value: round(float(value), 4)
                        )
                        st.dataframe(
                            results_df,
                            use_container_width=True,
                            hide_index=True,
                        )
                    else:
                        st.info("No headlines were returned for this topic.")
