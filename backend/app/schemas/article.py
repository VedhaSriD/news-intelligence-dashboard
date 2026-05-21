"""
schemas/article.py
Pydantic v2 schemas for API request validation and response serialization.
"""
from __future__ import annotations
from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


# ── Source ────────────────────────────────────────────────────────────────────

class SourceOut(BaseModel):
    id:                UUID
    name:              str
    slug:              str
    domain:            str
    credibility_score: float
    bias_label:        Optional[str]
    category:          Optional[str]
    country:           str
    # Populated dynamically in the sources route via a count query.
    # Defaults to 0 when not joined — never causes a validation error.
    article_count:     int = 0

    model_config = {"from_attributes": True}


# ── Article ───────────────────────────────────────────────────────────────────

class ArticleOut(BaseModel):
    id:                        UUID
    title:                     str
    summary:                   Optional[str]
    category:                  str
    source_name:               Optional[str]
    source_url:                Optional[str]
    canonical_url:             Optional[str]
    image_url:                 Optional[str]
    author:                    Optional[str]
    published_at:              datetime
    credibility_score:         float
    freshness_score:           float
    # composite_score is a Postgres GENERATED column — may be None on very new rows
    composite_score:           Optional[float] = None
    fact_check_status:         str
    is_breaking:               bool
    is_cluster_representative: bool
    duplicate_cluster_id:      Optional[UUID]
    cluster_source_count:      int
    tags:                      list[str]

    model_config = {"from_attributes": True}

    @field_validator("tags", mode="before")
    @classmethod
    def ensure_list(cls, v):
        return v or []


class ArticleDetail(ArticleOut):
    content_snippet: Optional[str]
    source:          Optional[SourceOut]


# ── Paginated ─────────────────────────────────────────────────────────────────

class PaginatedArticles(BaseModel):
    total:     int
    page:      int
    page_size: int
    results:   list[ArticleOut]


# ── Category ──────────────────────────────────────────────────────────────────

class CategoryInfo(BaseModel):
    slug:          str
    label:         str
    article_count: int
    latest_at:     Optional[datetime]


# ── Bookmarks ─────────────────────────────────────────────────────────────────

class BookmarkCreate(BaseModel):
    article_id: UUID


class BookmarkOut(BaseModel):
    id:         UUID
    article_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Health ────────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status:       str
    env:          str
    db_connected: bool
    latest_fetch: Optional[datetime]


# ── Fetch Run ─────────────────────────────────────────────────────────────────

class FetchRunOut(BaseModel):
    id:                    UUID
    started_at:            datetime
    completed_at:          Optional[datetime]
    status:                str
    articles_fetched:      int
    articles_inserted:     int
    articles_deduplicated: int
    error_message:         Optional[str]

    model_config = {"from_attributes": True}