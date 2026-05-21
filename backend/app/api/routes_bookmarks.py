"""
api/routes_bookmarks.py
Bookmark CRUD — requires Clerk authentication.
"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import require_user
from app.models.article import BookmarkedArticle, Article
from app.schemas.article import BookmarkCreate, BookmarkOut, ArticleOut

router = APIRouter(prefix="/api/v1/bookmarks", tags=["bookmarks"])


@router.get("", response_model=list[ArticleOut])
async def get_bookmarks(
    user_id: str     = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    """Returns all bookmarked articles for the authenticated user."""
    rows = (await db.execute(
        select(Article)
        .join(BookmarkedArticle, BookmarkedArticle.article_id == Article.id)
        .where(BookmarkedArticle.user_id == user_id)
        .order_by(BookmarkedArticle.created_at.desc())
    )).scalars().all()
    return [ArticleOut.model_validate(a) for a in rows]


@router.post("", response_model=BookmarkOut, status_code=201)
async def add_bookmark(
    body:    BookmarkCreate,
    user_id: str            = Depends(require_user),
    db: AsyncSession        = Depends(get_db),
):
    # Check article exists
    article = (await db.execute(
        select(Article).where(Article.id == body.article_id)
    )).scalar_one_or_none()
    if not article:
        raise HTTPException(404, "Article not found")

    # Avoid duplicate
    existing = (await db.execute(
        select(BookmarkedArticle).where(
            and_(
                BookmarkedArticle.user_id == user_id,
                BookmarkedArticle.article_id == body.article_id,
            )
        )
    )).scalar_one_or_none()
    if existing:
        return BookmarkOut.model_validate(existing)

    bm = BookmarkedArticle(user_id=user_id, article_id=body.article_id)
    db.add(bm)
    await db.commit()
    await db.refresh(bm)
    return BookmarkOut.model_validate(bm)


@router.delete("/{article_id}", status_code=204)
async def remove_bookmark(
    article_id: UUID,
    user_id:    str          = Depends(require_user),
    db: AsyncSession         = Depends(get_db),
):
    row = (await db.execute(
        select(BookmarkedArticle).where(
            and_(
                BookmarkedArticle.user_id == user_id,
                BookmarkedArticle.article_id == article_id,
            )
        )
    )).scalar_one_or_none()
    if not row:
        raise HTTPException(404, "Bookmark not found")
    await db.delete(row)
    await db.commit()