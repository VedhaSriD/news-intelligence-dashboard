"""
tests/conftest.py
Shared pytest fixtures for the full test suite.
"""
import pytest
from datetime import datetime, timezone, timedelta

from app.services.fetch_news import normalize_url, url_hash, normalize_title


def make_article(
    title:       str   = "Test Article About Technology",
    url:         str   = "https://example.com/article-1",
    category:    str   = "technology",
    hours_old:   float = 1.0,
    source_name: str   = "Reuters",
    credibility: float = 0.85,
    is_breaking: bool  = False,
) -> dict:
    """
    Central article factory used across all test files.
    Returns a normalized article dict that matches the structure
    expected by deduplicate_pipeline and classify_batch.
    """
    canonical = normalize_url(url)
    return {
        "title":                     title,
        "title_normalized":          normalize_title(title),
        "summary":                   "A test summary for this article.",
        "content_snippet":           (
            "This is a longer content snippet with more than 200 characters "
            "to test completeness scoring logic in the deduplication pipeline "
            "properly so that scoring thresholds are exercised correctly."
        ),
        "category":                  category,
        "source_name":               source_name,
        "source_url":                url,
        "canonical_url":             canonical,
        "url_hash":                  url_hash(canonical),
        "image_url":                 "https://example.com/image.jpg",
        "author":                    "Test Author",
        "published_at":              datetime.now(timezone.utc) - timedelta(hours=hours_old),
        "language":                  "en",
        "credibility_score":         credibility,
        "freshness_score":           0.90,
        "content_completeness":      0.70,
        "is_breaking":               is_breaking,
        "is_cluster_representative": False,
        "duplicate_cluster_id":      None,
        "cluster_source_count":      1,
        "tags":                      ["test", category],
    }


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def article_factory():
    """Returns the make_article factory function."""
    return make_article


@pytest.fixture
def sample_ai_article():
    return make_article(
        title="OpenAI launches new AI model for enterprise",
        url="https://techcrunch.com/openai-model",
        category="ai",
        source_name="TechCrunch",
        credibility=0.85,
    )


@pytest.fixture
def sample_politics_article():
    return make_article(
        title="Parliament votes on landmark climate legislation",
        url="https://bbc.com/parliament-climate",
        category="politics",
        source_name="BBC News",
        credibility=0.95,
    )


@pytest.fixture
def sample_breaking_article():
    return make_article(
        title="Breaking: Major earthquake strikes Southeast Asia",
        url="https://reuters.com/earthquake",
        category="world",
        source_name="Reuters",
        credibility=0.96,
        is_breaking=True,
        hours_old=0.1,
    )


@pytest.fixture
def near_duplicate_pair():
    """Two articles covering the same story from different sources."""
    a1 = make_article(
        title="Fed raises interest rates by 50 basis points",
        url="https://bloomberg.com/fed-rates",
        source_name="Bloomberg",
        credibility=0.90,
        category="business",
    )
    a2 = make_article(
        title="Fed raises interest rates by 50 basis points",
        url="https://reuters.com/fed-rates",
        source_name="Reuters",
        credibility=0.96,
        category="business",
    )
    return a1, a2


@pytest.fixture
def article_batch(article_factory):
    """
    A batch of 7 articles forming 5 distinct stories.
    Cluster 1: identical AI titles (2 articles) → 1 winner
    Cluster 2: identical Sports titles (2 articles) → 1 winner
    Unique: Health, Politics, Technology (1 each)
    Expected after dedup: 5 winners, 2 deduplicated.
    """
    return [
        article_factory("OpenAI releases GPT-5", "https://tc.com/1",      "ai",         1.0, "TechCrunch", 0.85),
        article_factory("OpenAI releases GPT-5", "https://wired.com/1",   "ai",         1.2, "Wired",      0.87),
        article_factory("India wins cricket World Cup", "https://bbc.com/1",  "sports",  2.0, "BBC Sport",  0.90),
        article_factory("India wins cricket World Cup", "https://espn.com/1", "sports",  2.1, "ESPN",       0.85),
        article_factory("WHO approves new malaria vaccine",    "https://who.com/1",      "health",    3.0, "Reuters",  0.96),
        article_factory("Parliament passes digital economy bill","https://guardian.com/1","politics",  4.0, "Guardian", 0.88),
        article_factory("IBM reaches quantum computing milestone","https://space.com/1", "technology",5.0, "Wired",    0.87),
    ]