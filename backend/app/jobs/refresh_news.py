"""
jobs/refresh_news.py
Full pipeline: fetch → classify → deduplicate → summarize → fact-check → save.
Called by the scheduler and by POST /api/v1/jobs/refresh.
"""
import logging
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.article import Article, FetchRun, ArticleCluster
from app.services.fetch_news import fetch_all_articles
from app.services.classify import classify_batch
from app.services.deduplicate import deduplicate_pipeline
from app.services.summarize import batch_summarize
from app.services.credibility import batch_factcheck
from app.services.telegram_notifier import send_refresh_summary, send_breaking_alert

logger = logging.getLogger(__name__)


async def _load_known_hashes(db: AsyncSession) -> set[str]:
    result = await db.execute(select(Article.url_hash).where(Article.url_hash.isnot(None)))
    return {row[0] for row in result.all()}


async def _save_articles(db: AsyncSession, articles: list[dict]) -> int:
    known   = await _load_known_hashes(db)
    inserted= 0
    cluster_ids: set[str] = set()

    for a in articles:
        cid = a.get("duplicate_cluster_id")
        if cid and cid not in cluster_ids:
            db.add(ArticleCluster(
                id=cid,
                article_count=sum(1 for x in articles if x.get("duplicate_cluster_id") == cid)
            ))
            cluster_ids.add(cid)

    for a in articles:
        if a.get("url_hash") in known:
            continue
        db.add(Article(
            title=a["title"],
            title_normalized=a.get("title_normalized"),
            summary=a.get("summary"),
            content_snippet=a.get("content_snippet"),
            category=a["category"],
            source_name=a.get("source_name"),
            source_url=a.get("source_url"),
            canonical_url=a.get("canonical_url"),
            url_hash=a.get("url_hash"),
            image_url=a.get("image_url"),
            author=a.get("author"),
            published_at=a["published_at"],
            language=a.get("language", "en"),
            credibility_score=a.get("credibility_score", 0.70),
            freshness_score=a.get("freshness_score", 1.0),
            content_completeness=a.get("content_completeness", 0.5),
            duplicate_cluster_id=a.get("duplicate_cluster_id"),
            is_cluster_representative=a.get("is_cluster_representative", False),
            cluster_source_count=a.get("cluster_source_count", 1),
            is_breaking=a.get("is_breaking", False),
            fact_check_status=a.get("fact_check_status", "unchecked"),
            tags=a.get("tags"),
        ))
        inserted += 1

    await db.commit()
    return inserted


async def run_refresh_job() -> dict:
    async with AsyncSessionLocal() as db:
        run = FetchRun(status="running", started_at=datetime.now(timezone.utc))
        db.add(run)
        await db.commit()
        await db.refresh(run)

        try:
            raw         = await fetch_all_articles()
            run.articles_fetched = len(raw)

            classified  = classify_batch(raw)
            known       = await _load_known_hashes(db)
            processed, stats = deduplicate_pipeline(classified, known)

            winners     = [a for a in processed if a.get("is_cluster_representative")]
            winners     = await batch_summarize(winners)
            w_map       = {a["url_hash"]: a["summary"] for a in winners if a.get("url_hash")}
            for a in processed:
                if a.get("url_hash") in w_map:
                    a["summary"] = w_map[a["url_hash"]]

            processed   = await batch_factcheck(processed)
            inserted    = await _save_articles(db, processed)

            for a in processed:
                if a.get("is_breaking") and a.get("is_cluster_representative"):
                    await send_breaking_alert(a)

            run.status                 = "success"
            run.completed_at           = datetime.now(timezone.utc)
            run.articles_inserted      = inserted
            run.articles_deduplicated  = stats["deduplicated"]
            run.sources_used           = ["newsapi", "rss"]
            run.metadata_              = stats
            await db.commit()

            stats["inserted"] = inserted
            await send_refresh_summary(stats)
            return {"status": "success", "run_id": str(run.id), **stats}

        except Exception as e:
            logger.error(f"Refresh job failed: {e}", exc_info=True)
            run.status        = "failed"
            run.completed_at  = datetime.now(timezone.utc)
            run.error_message = str(e)
            await db.commit()
            return {"status": "failed", "error": str(e)}