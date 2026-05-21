"""
api/routes_articles.py
Article endpoints — latest feed, archive, search, detail.
"""
from datetime import datetime, timezone, timedelta
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, func, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.article import Article
from app.schemas.article import ArticleOut, ArticleDetail, PaginatedArticles

router = APIRouter(prefix="/api/v1/articles", tags=["articles"])

VALID_CATEGORIES = [
    "ai", "technology", "education", "politics",
    "business", "startups", "world", "sports", "health",
]

@router.get("/latest")
async def get_latest():
    return {
        "total": 1,
        "page": 1,
        "page_size": 20,
        "results": [
            {
                "id": "1",
                "title": "NewsIntel API Working",
                "summary": "Backend connected successfully.",
                "category": "technology",
                "source_name": "Demo Source",
                "canonical_url": "https://example.com",
                "published_at": "2026-05-21T07:00:00Z",
                "credibility_score": 0.95,
                "freshness_score": 0.90,
                "composite_score": 0.92,
                "fact_check_status": "clear",
                "is_breaking": False,
                "cluster_source_count": 1,
                "tags": ["demo"]
            }
        ]
    }


@router.get("/archive", response_model=PaginatedArticles)
async def get_archive(
    date:      str           = Query(..., description="YYYY-MM-DD"),
    category:  Optional[str] = Query(None),
    page:      int           = Query(1, ge=1),
    page_size: int           = Query(20, ge=5, le=100),
    db: AsyncSession         = Depends(get_db),
):
    try:
        target = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        raise HTTPException(400, "Invalid date. Use YYYY-MM-DD")

    conditions = [
        Article.published_at >= target,
        Article.published_at < target + timedelta(days=1),
        Article.is_cluster_representative == True,
    ]
    if category:
        conditions.append(Article.category == category)

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
        total=total, page=page, page_size=page_size,
        results=[ArticleOut.model_validate(a) for a in results],
    )


@router.get("/search", response_model=PaginatedArticles)
async def search_articles(
    q:         str           = Query(..., min_length=2),
    category:  Optional[str] = Query(None),
    page:      int           = Query(1, ge=1),
    page_size: int           = Query(20, ge=5, le=50),
    db: AsyncSession         = Depends(get_db),
):
    conditions = [
        Article.title.ilike(f"%{q}%"),
        Article.is_cluster_representative == True,
    ]
    if category:
        conditions.append(Article.category == category)

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
        total=total, page=page, page_size=page_size,
        results=[ArticleOut.model_validate(a) for a in results],
    )


@router.get("/{article_id}", response_model=ArticleDetail)
async def get_article(
    article_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = (await db.execute(
        select(Article)
        .where(Article.id == article_id)
        .options(selectinload(Article.source))
    )).scalar_one_or_none()

    if not result:
        raise HTTPException(404, "Article not found")
    return ArticleDetail.model_validate(result)