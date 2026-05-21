"""
models/article.py
SQLAlchemy ORM models — map directly to the database tables in schema.sql.
"""
import uuid
from sqlalchemy import (
    Column, String, Text, Boolean, DateTime, Numeric,
    ForeignKey, ARRAY, JSON, Integer, func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class Source(Base):
    __tablename__ = "sources"

    id                = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name              = Column(String(255), nullable=False)
    slug              = Column(String(100), unique=True, nullable=False)
    domain            = Column(String(255), nullable=False)
    rss_url           = Column(Text)
    newsapi_id        = Column(String(100))
    category          = Column(String(50))
    language          = Column(String(2), default="en")
    country           = Column(String(2), default="us")
    credibility_score = Column(Numeric(3, 2), default=0.70)
    bias_label        = Column(String(50))
    is_active         = Column(Boolean, default=True)
    created_at        = Column(DateTime(timezone=True), server_default=func.now())
    updated_at        = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    articles = relationship("Article", back_populates="source")


class ArticleCluster(Base):
    __tablename__ = "article_clusters"

    id                        = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_summary             = Column(Text)
    representative_article_id = Column(UUID(as_uuid=True))
    article_count             = Column(Integer, default=0)
    first_seen_at             = Column(DateTime(timezone=True), server_default=func.now())
    last_updated_at           = Column(DateTime(timezone=True), server_default=func.now())

    articles = relationship("Article", back_populates="cluster")


class Article(Base):
    __tablename__ = "articles"

    id                        = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title                     = Column(Text, nullable=False)
    title_normalized          = Column(Text)
    summary                   = Column(Text)
    content_snippet           = Column(Text)
    category                  = Column(String(50), nullable=False)
    source_id                 = Column(UUID(as_uuid=True), ForeignKey("sources.id", ondelete="SET NULL"))
    source_name               = Column(String(255))
    source_url                = Column(Text)
    canonical_url             = Column(Text)
    url_hash                  = Column(String(64), unique=True)
    image_url                 = Column(Text)
    author                    = Column(Text)
    published_at              = Column(DateTime(timezone=True), nullable=False)
    language                  = Column(String(2), default="en")
    country                   = Column(String(2), default="global")
    credibility_score         = Column(Numeric(3, 2), default=0.70)
    freshness_score           = Column(Numeric(3, 2), default=1.00)
    content_completeness      = Column(Numeric(3, 2), default=0.50)
    # composite_score is a GENERATED column in Postgres — read-only from ORM
    composite_score           = Column(Numeric(3, 2), nullable=True)
    duplicate_cluster_id      = Column(UUID(as_uuid=True), ForeignKey("article_clusters.id", ondelete="SET NULL"))
    is_cluster_representative = Column(Boolean, default=False)
    cluster_source_count      = Column(Integer, default=1)
    fact_check_status         = Column(String(30), default="unchecked")
    is_breaking               = Column(Boolean, default=False)
    tags                      = Column(ARRAY(Text))
    raw_data                  = Column(JSON)
    created_at                = Column(DateTime(timezone=True), server_default=func.now())
    updated_at                = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    source  = relationship("Source",         back_populates="articles")
    cluster = relationship("ArticleCluster", back_populates="articles")


class FetchRun(Base):
    __tablename__ = "fetch_runs"

    id                    = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    started_at            = Column(DateTime(timezone=True), server_default=func.now())
    completed_at          = Column(DateTime(timezone=True))
    status                = Column(String(20), default="running")
    articles_fetched      = Column(Integer, default=0)
    articles_inserted     = Column(Integer, default=0)
    articles_deduplicated = Column(Integer, default=0)
    error_message         = Column(Text)
    sources_used          = Column(ARRAY(Text))
    metadata_             = Column("metadata", JSON)


class BookmarkedArticle(Base):
    __tablename__ = "bookmarked_articles"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id    = Column(String(255), nullable=False)
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FactCheck(Base):
    __tablename__ = "fact_checks"

    id                = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id        = Column(UUID(as_uuid=True), ForeignKey("articles.id", ondelete="CASCADE"))
    claim_text        = Column(Text, nullable=False)
    claim_rating      = Column(String(100))
    fact_checker_name = Column(String(255))
    fact_checker_url  = Column(Text)
    review_url        = Column(Text)
    checked_at        = Column(DateTime(timezone=True), server_default=func.now())