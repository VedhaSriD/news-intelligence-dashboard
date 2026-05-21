"""
api/routes_categories.py
Category list and per-category article feed.
"""
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, func, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.article import Article
from app.schemas.article import CategoryInfo, PaginatedArticles, ArticleOut

router = APIRouter(prefix="/api/v1/categories", tags=["categories"])

CATEGORY_LABELS = {
    "ai":         "AI & ML",
    "technology": "Technology",
    "education":  "Education",
    "politics":   "Politics",
    "business":   "Business",
    "startups":   "Startups",
    "world":      "World News",
    "sports":     "Sports",
    "health":     "Health & Science",
}

ALL_SLUGS = list(CATEGORY_LABELS.keys())


@router.get("", response_model=list[CategoryInfo])
async def list_categories(db: AsyncSession = Depends(get_db)):
    """Returns all categories with article counts for the last 24 hours."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

    rows = (await db.execute(
        select(
            Article.category,
            func.count(Article.id).label("article_count"),
            func.max(Article.published_at).label("latest_at"),
        )
        .where(Article.published_at >= cutoff)
        .group_by(Article.category)
        .order_by(desc("article_count"))
    )).all()

    seen   = {row.category for row in rows}
    result = [
        CategoryInfo(
            slug=row.category,
            label=CATEGORY_LABELS.get(row.category, row.category.title()),
            article_count=row.article_count,
            latest_at=row.latest_at,
        )
        for row in rows
    ]
    for slug in ALL_SLUGS:
        if slug not in seen:
            result.append(CategoryInfo(
                slug=slug,
                label=CATEGORY_LABELS[slug],
                article_count=0,
                latest_at=None,
            ))
    return result


@router.get("/{slug}/articles", response_model=PaginatedArticles)
async def category_articles(
    slug:      str,
    hours:     int = Query(24, ge=1, le=72),
    page:      int = Query(1, ge=1),
    page_size: int = Query(20, ge=5, le=100),
    db: AsyncSession = Depends(get_db),
):
    if slug not in ALL_SLUGS:
        raise HTTPException(status_code=404, detail=f"Unknown category: {slug}")

    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    conditions = [
        Article.category == slug,
        Article.published_at >= cutoff,
        Article.is_cluster_representative == True,
    ]

    total = (await db.execute(
        select(func.count()).select_from(Article).where(and_(*conditions))
    )).scalar_one()

    results = (await db.execute(
        select(Article)
        .where(and_(*conditions))
        .order_by(desc(Article.published_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )).scalars().all()

    return PaginatedArticles(
        total=total,
        page=page,
        page_size=page_size,
        results=[ArticleOut.model_validate(a) for a in results],
    )