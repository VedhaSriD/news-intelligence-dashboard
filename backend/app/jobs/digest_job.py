"""
jobs/digest_job.py
Sends top-10 articles as a Telegram digest at 08:00 UTC daily.
"""
import logging
from datetime import datetime, timezone, timedelta

from sqlalchemy import select, desc, and_

from app.core.database import AsyncSessionLocal
from app.models.article import Article
from app.services.telegram_notifier import send_daily_digest

logger = logging.getLogger(__name__)


async def run_digest_job() -> dict:
    async with AsyncSessionLocal() as db:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        results= (await db.execute(
            select(Article)
            .where(and_(Article.published_at >= cutoff, Article.is_cluster_representative == True))
            .order_by(desc(Article.credibility_score))
            .limit(10)
        )).scalars().all()

    if not results:
        return {"status": "skipped", "reason": "no articles"}

    articles_dicts = [
        {
            "title":       a.title,
            "category":    a.category,
            "source_name": a.source_name,
            "canonical_url": a.canonical_url or a.source_url,
            "credibility_score": float(a.credibility_score or 0),
        }
        for a in results
    ]
    ok = await send_daily_digest(articles_dicts)
    return {"status": "sent" if ok else "failed", "count": len(articles_dicts)}