"""
services/fetch_news.py
Fetches articles from NewsAPI and RSS feeds.
Returns normalized article dicts ready for the deduplication pipeline.
"""
import hashlib
import re
import logging
from datetime import datetime, timezone
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

import httpx
import feedparser
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import get_settings

logger   = logging.getLogger(__name__)
settings = get_settings()

CATEGORY_QUERIES = {
    "ai":         "artificial intelligence OR machine learning OR OpenAI OR Anthropic OR LLM",
    "technology": "technology OR software OR cybersecurity OR cloud computing OR semiconductor",
    "education":  "education OR university OR learning OR EdTech OR scholarship",
    "politics":   "politics OR government OR election OR policy OR parliament",
    "business":   "business OR economy OR market OR finance OR trade",
    "startups":   "startup OR venture capital OR funding OR IPO OR founder",
    "world":      "world news OR international OR global crisis",
    "sports":     "sports OR football OR cricket OR basketball OR tennis",
    "health":     "health OR medicine OR pandemic OR WHO OR clinical trial",
}

RSS_FEEDS = {
    "ai":         ["https://www.technologyreview.com/feed/"],
    "technology": ["https://feeds.arstechnica.com/arstechnica/index"],
    "world":      ["https://feeds.bbci.co.uk/news/world/rss.xml"],
    "health":     ["https://www.who.int/rss-feeds/news-english.xml"],
    "sports":     ["https://feeds.bbci.co.uk/sport/rss.xml"],
}


def normalize_url(url: str) -> str:
    """Strips tracking params (utm_*, fbclid, etc.) from a URL."""
    STRIP = {
        "utm_source", "utm_medium", "utm_campaign", "utm_term",
        "utm_content", "fbclid", "gclid", "ref", "source", "_ga",
    }
    try:
        p  = urlparse(url)
        qs = parse_qs(p.query, keep_blank_values=False)
        cq = {k: v for k, v in qs.items() if k.lower() not in STRIP}
        return urlunparse(p._replace(query=urlencode(cq, doseq=True), fragment=""))
    except Exception:
        return url


def url_hash(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", title.lower()).strip()


def parse_date(date_str: str | None) -> datetime:
    if not date_str:
        return datetime.now(timezone.utc)
    fmts = [
        "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z",
        "%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S %z",
    ]
    for fmt in fmts:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return datetime.now(timezone.utc)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
async def fetch_newsapi(category: str, query: str) -> list[dict]:
    if not settings.newsapi_key:
        return []
    params = {
        "q": query, "language": "en",
        "sortBy": "publishedAt", "pageSize": 30,
        "apiKey": settings.newsapi_key,
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get("https://newsapi.org/v2/everything", params=params)
        resp.raise_for_status()
        data = resp.json()

    articles = []
    for item in data.get("articles", []):
        url = item.get("url", "")
        if not url or url == "https://removed.com":
            continue
        canonical = normalize_url(url)
        articles.append({
            "title":            (item.get("title") or "").strip(),
            "title_normalized": normalize_title(item.get("title") or ""),
            "summary":          None,
            "content_snippet":  (item.get("content") or item.get("description") or "")[:500],
            "category":         category,
            "source_name":      item.get("source", {}).get("name", "Unknown"),
            "source_url":       url,
            "canonical_url":    canonical,
            "url_hash":         url_hash(canonical),
            "image_url":        item.get("urlToImage"),
            "author":           item.get("author"),
            "published_at":     parse_date(item.get("publishedAt")),
            "language":         "en",
            "raw_data":         None,
        })
    logger.info(f"NewsAPI: {len(articles)} articles for '{category}'")
    return articles


async def fetch_rss(category: str, feed_url: str) -> list[dict]:
    try:
        feed = feedparser.parse(feed_url)
        articles = []
        for entry in feed.entries[:15]:
            url = entry.get("link", "")
            if not url:
                continue
            canonical = normalize_url(url)
            title     = entry.get("title", "").strip()
            articles.append({
                "title":            title,
                "title_normalized": normalize_title(title),
                "summary":          None,
                "content_snippet":  (entry.get("summary") or "")[:500],
                "category":         category,
                "source_name":      feed.feed.get("title", "RSS Feed"),
                "source_url":       url,
                "canonical_url":    canonical,
                "url_hash":         url_hash(canonical),
                "image_url":        None,
                "author":           entry.get("author"),
                "published_at":     parse_date(entry.get("published") or entry.get("updated")),
                "language":         "en",
                "raw_data":         None,
            })
        return articles
    except Exception as e:
        logger.error(f"RSS fetch failed {feed_url}: {e}")
        return []


async def fetch_all_articles() -> list[dict]:
    all_articles = []
    for cat, q in CATEGORY_QUERIES.items():
        try:
            all_articles.extend(await fetch_newsapi(cat, q))
        except Exception as e:
            logger.error(f"NewsAPI failed for {cat}: {e}")
    for cat, feeds in RSS_FEEDS.items():
        for feed_url in feeds:
            all_articles.extend(await fetch_rss(cat, feed_url))
    logger.info(f"Total raw articles fetched: {len(all_articles)}")
    return all_articles