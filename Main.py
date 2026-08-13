"""
Fetch public Google Play reviews for the Roblox Android app
(com.roblox.client), run Hugging Face transformer sentiment analysis
(cardiffnlp/twitter-roberta-base-sentiment-latest), save results to CSV,
and produce a sentiment distribution chart plus an executive summary.
"""

import re
import sys
from collections import Counter

import matplotlib

matplotlib.use("Agg")  # headless backend: render charts without a display window
import matplotlib.pyplot as plt
import pandas as pd
import torch
from google_play_scraper import Sort, reviews
from transformers import logging as tf_logging, pipeline

# Suppress non-critical transformer logging warnings
tf_logging.set_verbosity_error()

# Roblox's Google Play app ID (Android app package name)
PLAY_APP_ID = "com.roblox.client"

# Model name for Hugging Face sentiment analysis
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

# Common English stopwords to ignore when counting review words
STOPWORDS = {
    "a", "about", "an", "and", "are", "as", "at", "be", "been", "but", "by",
    "can", "did", "do", "does", "for", "from", "get", "got", "had", "has",
    "have", "he", "her", "his", "i", "if", "in", "is", "it", "its", "just",
    "me", "my", "no", "not", "of", "on", "or", "our", "she", "so", "that",
    "the", "their", "them", "then", "there", "these", "they", "this", "to",
    "too", "up", "us", "was", "we", "were", "what", "when", "which", "will",
    "with", "you", "your",
}


def fetch_roblox_reviews(limit: int = 100) -> pd.DataFrame:
    """Fetch up to `limit` recent public Play Store reviews for Roblox.

    Returns a DataFrame with columns:
        reviews_text   - the review body text
        rating         - the reviewer's 1-5 star rating
        timestamp      - review creation date formatted as YYYY-MM-DD
    """
    # Query google-play-scraper for the app's reviews. It returns a
    # (reviews_list, continuation_token) tuple; we only need the list.
    # lang='en' keeps the data English, suitable for English sentiment models.
    result, _ = reviews(
        PLAY_APP_ID,
        lang="en",        # review language
        country="us",     # store country
        sort=Sort.NEWEST, # most recent reviews first
        count=limit,      # number of reviews to fetch
    )

    # Flatten each raw review into the three fields we care about.
    rows = [
        {
            "reviews_text": review["content"],  # the review body text
            "rating": review["score"],          # 1-5 star rating
            # "at" is a datetime; format it as a plain date string
            "timestamp": review["at"].strftime("%Y-%m-%d"),
        }
        for review in result
    ]

    # Build the DataFrame with the exact column order specified.
    df = pd.DataFrame(rows, columns=["reviews_text", "rating", "timestamp"])
    return df


def analyze_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """Add Hugging Face RoBERTa sentiment predictions to each review.

    Adds the columns:
        sentiment_label  - "positive", "neutral", or "negative"
        sentiment_score  - confidence score for the predicted sentiment
    """
    device = 0 if torch.cuda.is_available() else -1
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model=MODEL_NAME,
        device=device,
        truncation=True,
        max_length=512,
    )

    # Ensure all review texts are valid non-empty strings
    texts = [
        str(t).strip() if pd.notna(t) and str(t).strip() else "N/A"
        for t in df["reviews_text"]
    ]

    with torch.no_grad():
        results = sentiment_pipeline(texts, batch_size=16)

    df["sentiment_label"] = [r["label"].lower() for r in results]
    df["sentiment_score"] = [r["score"] for r in results]

    return df


def plot_sentiment_distribution(df: pd.DataFrame, filename: str = "sentiment_chart.png") -> None:
    """Draw a bar chart of the sentiment_label counts and save it as a PNG."""
    counts = df["sentiment_label"].value_counts()
    labels = ["positive", "neutral", "negative"]
    values = [counts.get(label, 0) for label in labels]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, values, color=["#2ecc71", "#f1c40f", "#e74c3c"])

    total = len(df)
    for bar, value in zip(bars, values):
        pct = 100.0 * value / total if total else 0.0
        ax.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f"{value}\n({pct:.1f}%)",
            ha="center", va="bottom",
        )

    ax.set_title("Sentiment Distribution of Roblox Reviews")
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Number of Reviews")
    ax.set_ylim(0, max(values) * 1.15 if values else 1)

    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)  # free memory; the chart is already on disk


def top_words(reviews_texts: pd.Series, n: int = 5) -> list[tuple[str, int]]:
    """Return the `n` most frequent non-stopword tokens in the given texts."""
    counter = Counter()
    for text in reviews_texts:
        words = re.findall(r"[a-z']+", str(text).lower())
        counter.update(w for w in words if w not in STOPWORDS and len(w) > 1)
    return counter.most_common(n)


def print_summary(df: pd.DataFrame) -> None:
    """Print the executive summary: totals, percentages, top words per class."""
    total = len(df)
    print("=" * 60)
    print("EXECUTIVE SUMMARY - Roblox Google Play Reviews")
    print("=" * 60)

    print(f"Total reviews analyzed: {total}")
    counts = df["sentiment_label"].value_counts()
    for label in ["positive", "neutral", "negative"]:
        count = counts.get(label, 0)
        pct = 100.0 * count / total if total else 0.0
        print(f"  {label:<8}: {count:>3} reviews ({pct:.1f}%)")

    negative_texts = df.loc[df["sentiment_label"] == "negative", "reviews_text"]
    positive_texts = df.loc[df["sentiment_label"] == "positive", "reviews_text"]

    print("\nTop 5 words in NEGATIVE reviews:")
    for word, count in top_words(negative_texts):
        print(f"  {word:<15} {count}")
    print("\nTop 5 words in POSITIVE reviews:")
    for word, count in top_words(positive_texts):
        print(f"  {word:<15} {count}")
    print("=" * 60)


if __name__ == "__main__":
    # Windows consoles default to cp1252 and crash on non-ASCII review text;
    # force UTF-8 so printing unicode (emoji, CJK) works everywhere.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Full workflow: fetch -> analyze -> save CSV -> chart -> summary.
    df = fetch_roblox_reviews(limit=100)
    df = analyze_sentiment(df)

    # Save DataFrame to CSV with encoding utf-8-sig
    df.to_csv("roblox_sentiment_reviews.csv", index=False, encoding="utf-8-sig")

    # Save distribution chart as sentiment_chart.png
    plot_sentiment_distribution(df, filename="sentiment_chart.png")

    print_summary(df)
    print("\nDataFrame saved to roblox_sentiment_reviews.csv")
    print("Chart saved to sentiment_chart.png")
