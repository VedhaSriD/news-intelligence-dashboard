"""
services/classify.py
Keyword-based article classifier.
Corrects mislabeled articles after ingestion.
"""
import re
import logging

logger = logging.getLogger(__name__)

KEYWORDS: dict[str, dict[str, float]] = {
    "ai": {
        "artificial intelligence": 3.0, "machine learning": 3.0, "llm": 3.0,
        "openai": 2.0, "anthropic": 2.0, "chatgpt": 2.0, "gpt": 2.0,
        "generative ai": 2.5, "foundation model": 2.0, "neural network": 2.5,
        "deep learning": 2.5, "claude": 1.5, "gemini": 1.5, "agi": 2.5,
    },
    "technology": {
        "software": 1.5, "hardware": 1.5, "cybersecurity": 2.0,
        "cloud computing": 2.0, "semiconductor": 2.0, "chip": 1.5,
        "data breach": 2.0, "encryption": 1.5, "quantum computing": 2.5,
        "developer": 1.5, "5g": 1.5, "apple": 1.0, "google": 1.0,
    },
    "education": {
        "university": 2.0, "school": 1.5, "student": 1.5, "education": 2.5,
        "curriculum": 2.0, "edtech": 2.5, "scholarship": 2.0, "tuition": 2.0,
        "professor": 1.5, "academic": 1.5, "degree": 1.5, "campus": 1.5,
    },
    "politics": {
        "government": 2.0, "election": 3.0, "parliament": 2.5,
        "president": 2.0, "prime minister": 2.5, "congress": 2.0,
        "senate": 2.0, "legislation": 2.0, "vote": 2.0, "minister": 1.5,
        "sanction": 2.0, "treaty": 2.0, "geopolit": 2.0, "diplomat": 1.5,
    },
    "business": {
        "economy": 2.0, "market": 1.5, "stock": 1.5, "finance": 2.0,
        "gdp": 2.5, "inflation": 2.5, "interest rate": 2.5, "merger": 2.5,
        "acquisition": 2.5, "earnings": 2.0, "ipo": 2.5, "revenue": 1.5,
        "recession": 2.5, "supply chain": 2.0, "trade war": 2.0,
    },
    "startups": {
        "startup": 3.0, "venture capital": 3.0, "funding round": 3.0,
        "series a": 2.5, "series b": 2.5, "valuation": 2.0, "founder": 2.0,
        "unicorn": 2.5, "y combinator": 2.5, "accelerator": 2.0, "pitch": 1.5,
    },
    "world": {
        "war": 2.5, "conflict": 2.0, "crisis": 1.5, "united nations": 2.5,
        "nato": 2.5, "refugee": 2.5, "humanitarian": 2.0, "disaster": 2.0,
        "earthquake": 2.5, "flood": 2.0, "g7": 2.5, "g20": 2.5, "summit": 2.0,
    },
    "sports": {
        "football": 2.5, "soccer": 2.5, "cricket": 2.5, "basketball": 2.5,
        "tennis": 2.5, "golf": 2.0, "olympic": 3.0, "championship": 2.0,
        "tournament": 2.0, "fifa": 3.0, "nba": 3.0, "nfl": 3.0, "ipl": 2.5,
    },
    "health": {
        "health": 2.0, "medicine": 2.0, "hospital": 2.0, "vaccine": 2.5,
        "pandemic": 3.0, "disease": 2.0, "cancer": 2.5, "clinical trial": 3.0,
        "fda": 2.5, "who": 2.0, "mental health": 2.5, "pharmaceutical": 2.5,
        "biotech": 2.0, "nutrition": 1.5,
    },
}

MIN_SCORE = 2.0


def classify_article(title: str, content: str = "", original: str = "world") -> str:
    text = re.sub(r"[^\w\s]", " ", f"{title} {content}".lower())
    best_cat, best_score = original, 0.0
    for cat, kws in KEYWORDS.items():
        score = sum(
            weight * (1.5 if kw in title.lower() else 1.0)
            for kw, weight in kws.items()
            if kw in text
        )
        if score > best_score:
            best_score = score; best_cat = cat
    return best_cat if best_score >= MIN_SCORE else original


def classify_batch(articles: list[dict]) -> list[dict]:
    corrected = 0
    for a in articles:
        orig   = a.get("category", "world")
        new_cat= classify_article(a.get("title", ""), a.get("content_snippet", ""), orig)
        if new_cat != orig:
            a["category"] = new_cat; corrected += 1
    logger.info(f"Classifier: corrected {corrected}/{len(articles)} categories")
    return articles