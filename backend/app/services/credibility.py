"""
services/credibility.py
Optional Google Fact Check Tools API integration.
"""
import logging
from typing import Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import get_settings

logger   = logging.getLogger(__name__)
settings = get_settings()

FACTCHECK_URL  = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
FLAGGED_RATINGS= {"false", "mostly false", "misleading", "pants on fire", "incorrect", "fabricated"}


@retry(stop=stop_after_attempt(2), wait=wait_exponential(min=1, max=5))
async def check_claim(query: str) -> Optional[dict]:
    if not settings.google_factcheck_api_key:
        return None
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(FACTCHECK_URL, params={
                "query": query[:200], "key": settings.google_factcheck_api_key,
                "languageCode": "en", "pageSize": 3,
            })
            if resp.status_code == 200:
                claims = resp.json().get("claims", [])
                if claims:
                    review = claims[0].get("claimReview", [{}])[0]
                    return {
                        "claim_text":        claims[0].get("text", ""),
                        "claim_rating":      review.get("textualRating", "Unknown"),
                        "fact_checker_name": review.get("publisher", {}).get("name", ""),
                        "fact_checker_url":  review.get("publisher", {}).get("site", ""),
                        "review_url":        review.get("url", ""),
                    }
    except Exception as e:
        logger.warning(f"Fact check error: {e}")
    return None


async def enrich_factcheck(article: dict) -> dict:
    result = await check_claim(article.get("title", ""))
    if result is None:
        article["fact_check_status"] = "clear"
    else:
        rating = (result.get("claim_rating") or "").lower()
        if any(r in rating for r in FLAGGED_RATINGS):
            article["fact_check_status"] = "flagged"
            article["credibility_score"] = max(0.0, article.get("credibility_score", 0.7) - 0.2)
        else:
            article["fact_check_status"] = "clear"
    return article


async def batch_factcheck(articles: list[dict], max_checks: int = 10) -> list[dict]:
    winners = sorted(
        [a for a in articles if a.get("is_cluster_representative")],
        key=lambda x: x.get("credibility_score", 0), reverse=True,
    )[:max_checks]
    for a in winners:
        await enrich_factcheck(a)
    return articles