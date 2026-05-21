"""
api/routes_admin.py
Admin endpoints for monitoring fetch runs and system stats.
Not protected in v1 — add auth middleware before production.
"""
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.article import Article, FetchRun, Source
from app.schemas.article import FetchRunOut, SourceOut

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.get("/fetch-runs", response_model=list[FetchRunOut])
async def list_fetch_runs(
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    runs = (await db.execute(
        select(FetchRun).order_by(desc(FetchRun.started_at)).limit(limit)
    )).scalars().all()
    return [FetchRunOut.model_validate(r) for r in runs]


@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

    total   = (await db.execute(select(func.count(Article.id)))).scalar_one()
    recent  = (await db.execute(
        select(func.count(Article.id)).where(Article.created_at >= cutoff)
    )).scalar_one()
    breaking= (await db.execute(
        select(func.count(Article.id)).where(
            and_(Article.is_breaking == True, Article.created_at >= cutoff)
        )
    )).scalar_one()
    avg_cred= (await db.execute(select(func.avg(Article.credibility_score)))).scalar_one()
    sources = (await db.execute(
        select(func.count(Source.id)).where(Source.is_active == True)
    )).scalar_one()
    last_fetch = (await db.execute(
        select(FetchRun.completed_at)
        .where(FetchRun.status == "success")
        .order_by(desc(FetchRun.completed_at))
        .limit(1)
    )).scalar_one_or_none()

    cat_rows = (await db.execute(
        select(Article.category, func.count(Article.id).label("cnt"))
        .group_by(Article.category)
        .order_by(desc("cnt"))
    )).all()

    return {
        "total_articles":       total,
        "articles_last_24h":    recent,
        "breaking_last_24h":    breaking,
        "avg_credibility_score": round(float(avg_cred or 0), 3),
        "active_sources":       sources,
        "last_successful_fetch":last_fetch,
        "categories":           {r.category: r.cnt for r in cat_rows},
    }