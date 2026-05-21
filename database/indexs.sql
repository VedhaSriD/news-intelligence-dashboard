-- ============================================================
-- NewsIntel — Indexes
-- Run after schema.sql
-- ============================================================

-- Articles: primary access patterns
CREATE INDEX IF NOT EXISTS idx_articles_category
    ON articles(category);

CREATE INDEX IF NOT EXISTS idx_articles_published_at
    ON articles(published_at DESC);

CREATE INDEX IF NOT EXISTS idx_articles_category_published
    ON articles(category, published_at DESC);

CREATE INDEX IF NOT EXISTS idx_articles_composite_score
    ON articles(composite_score DESC);

CREATE INDEX IF NOT EXISTS idx_articles_url_hash
    ON articles(url_hash);

CREATE INDEX IF NOT EXISTS idx_articles_cluster_id
    ON articles(duplicate_cluster_id);

CREATE INDEX IF NOT EXISTS idx_articles_is_representative
    ON articles(is_cluster_representative)
    WHERE is_cluster_representative = TRUE;

CREATE INDEX IF NOT EXISTS idx_articles_is_breaking
    ON articles(is_breaking)
    WHERE is_breaking = TRUE;

-- Full-text search using trigram index
CREATE INDEX IF NOT EXISTS idx_articles_title_trgm
    ON articles USING gin(title_normalized gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_articles_tags
    ON articles USING gin(tags);

-- Bookmarks
CREATE INDEX IF NOT EXISTS idx_bookmarks_user_id
    ON bookmarked_articles(user_id);

-- Fetch runs
CREATE INDEX IF NOT EXISTS idx_fetch_runs_started
    ON fetch_runs(started_at DESC);

CREATE INDEX IF NOT EXISTS idx_fetch_runs_status
    ON fetch_runs(status);

-- Sources
CREATE INDEX IF NOT EXISTS idx_sources_slug
    ON sources(slug);

CREATE INDEX IF NOT EXISTS idx_sources_active
    ON sources(is_active)
    WHERE is_active = TRUE;