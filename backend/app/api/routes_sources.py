"""
api/routes_sources.py
Source list endpoint — includes live article_count per source.
"""
from fastapi import APIRouter, Depends
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.article import Source, Article
from app.schemas.article import SourceOut

router = APIRouter(prefix="/api/v1/sources", tags=["sources"])


@router.get("", response_model=list[SourceOut])
async def list_sources(db: AsyncSession = Depends(get_db)):
    """
    Returns active sources ordered by credibility.
    article_count is calculated via a subquery so SourceOut.article_count
    is always populated correctly rather than defaulting to 0.
    """
    # Subquery: count articles per source
    article_counts = (
        select(Article.source_id, func.count(Article.id).label("cnt"))
        .group_by(Article.source_id)
        .subquery()
    )

    rows = (await db.execute(
        select(Source, func.coalesce(article_counts.c.cnt, 0).label("article_count"))
        .outerjoin(article_counts, article_counts.c.source_id == Source.id)
        .where(Source.is_active == True)
        .order_by(desc(Source.credibility_score))
    )).all()

    result = []
    for source, count in rows:
        out            = SourceOut.model_validate(source)
        out.article_count = int(count)
        result.append(out)
    return result