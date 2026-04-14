from collections import Counter

def sentiment_distribution(results):
    if not results:
        return {}

    sentiments = [r["sentiment"] for r in results]

    counts = Counter(sentiments)

    total = len(results)

    distribution = {}

    for sentiment, count in counts.items():
        distribution[sentiment] = round((count / total) * 100, 2)

    return distribution


### Keywords Extraction 

import re

stopwords = {
    "the","is","are","a","an","and","to","of","in","on","for","with","that"
}

def extract_keywords(texts, top_n=5):

    words = []

    for text in texts:

        cleaned = re.sub(r"[^a-zA-Z ]", "", text.lower())

        for word in cleaned.split():

            if word not in stopwords and len(word) > 2:
                words.append(word)

    common = Counter(words).most_common(top_n)

    return [word for word, count in common]
