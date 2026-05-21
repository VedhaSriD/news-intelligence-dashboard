-- ============================================================
-- NewsIntel — PostgreSQL Schema
-- Run: psql news_intel < database/schema.sql
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ── Users (mirrors Clerk user data) ──────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id         VARCHAR(255) PRIMARY KEY,   -- Clerk user_id
    email      VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name  VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ── User preferences ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user_preferences (
    id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id            VARCHAR(255) REFERENCES users(id) ON DELETE CASCADE,
    preferred_categories TEXT[],
    email_digest       BOOLEAN DEFAULT FALSE,
    telegram_alerts    BOOLEAN DEFAULT FALSE,
    created_at         TIMESTAMPTZ DEFAULT NOW(),
    updated_at         TIMESTAMPTZ DEFAULT NOW()
);

-- ── Sources ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sources (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name              VARCHAR(255) NOT NULL,
    slug              VARCHAR(100) UNIQUE NOT NULL,
    domain            VARCHAR(255) NOT NULL,
    rss_url           TEXT,
    newsapi_id        VARCHAR(100),
    category          VARCHAR(50),
    language          CHAR(2) DEFAULT 'en',
    country           CHAR(2) DEFAULT 'us',
    credibility_score DECIMAL(3,2) DEFAULT 0.70,
    bias_label        VARCHAR(50),
    is_active         BOOLEAN DEFAULT TRUE,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    updated_at        TIMESTAMPTZ DEFAULT NOW()
);

-- ── Article clusters (deduplication groups) ───────────────────
CREATE TABLE IF NOT EXISTS article_clusters (
    id                        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_summary             TEXT,
    representative_article_id UUID,
    article_count             INT DEFAULT 0,
    first_seen_at             TIMESTAMPTZ DEFAULT NOW(),
    last_updated_at           TIMESTAMPTZ DEFAULT NOW()
);

-- ── Articles ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS articles (
    id                        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title                     TEXT NOT NULL,
    title_normalized          TEXT,
    summary                   TEXT,
    content_snippet           TEXT,
    category                  VARCHAR(50) NOT NULL,
    source_id                 UUID REFERENCES sources(id) ON DELETE SET NULL,
    source_name               VARCHAR(255),
    source_url                TEXT,
    canonical_url             TEXT,
    url_hash                  CHAR(64) UNIQUE,
    image_url                 TEXT,
    author                    TEXT,
    published_at              TIMESTAMPTZ NOT NULL,
    language                  CHAR(2) DEFAULT 'en',
    country                   CHAR(2) DEFAULT 'global',
    credibility_score         DECIMAL(3,2) DEFAULT 0.70,
    freshness_score           DECIMAL(3,2) DEFAULT 1.00,
    content_completeness      DECIMAL(3,2) DEFAULT 0.50,
    composite_score           DECIMAL(3,2) GENERATED ALWAYS AS (
                                  credibility_score * 0.5 +
                                  freshness_score   * 0.3 +
                                  content_completeness * 0.2
                              ) STORED,
    duplicate_cluster_id      UUID REFERENCES article_clusters(id) ON DELETE SET NULL,
    is_cluster_representative BOOLEAN DEFAULT FALSE,
    cluster_source_count      INT DEFAULT 1,
    fact_check_status         VARCHAR(30) DEFAULT 'unchecked',
    is_breaking               BOOLEAN DEFAULT FALSE,
    tags                      TEXT[],
    raw_data                  JSONB,
    created_at                TIMESTAMPTZ DEFAULT NOW(),
    updated_at                TIMESTAMPTZ DEFAULT NOW()
);

-- ── Article categories (many-to-many alternative) ─────────────
CREATE TABLE IF NOT EXISTS article_categories (
    article_id  UUID REFERENCES articles(id) ON DELETE CASCADE,
    category    VARCHAR(50) NOT NULL,
    PRIMARY KEY (article_id, category)
);

-- ── Bookmarked articles ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS bookmarked_articles (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id    VARCHAR(255) NOT NULL,           -- Clerk user_id
    article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, article_id)
);

-- ── Fetch runs (scheduler logs) ───────────────────────────────
CREATE TABLE IF NOT EXISTS fetch_runs (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    started_at            TIMESTAMPTZ DEFAULT NOW(),
    completed_at          TIMESTAMPTZ,
    status                VARCHAR(20) DEFAULT 'running',
    articles_fetched      INT DEFAULT 0,
    articles_inserted     INT DEFAULT 0,
    articles_deduplicated INT DEFAULT 0,
    error_message         TEXT,
    sources_used          TEXT[],
    metadata              JSONB
);

-- ── Fact checks ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS fact_checks (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    article_id        UUID REFERENCES articles(id) ON DELETE CASCADE,
    claim_text        TEXT NOT NULL,
    claim_rating      VARCHAR(100),
    fact_checker_name VARCHAR(255),
    fact_checker_url  TEXT,
    review_url        TEXT,
    checked_at        TIMESTAMPTZ DEFAULT NOW()
);

-- ── Updated-at trigger ────────────────────────────────────────
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_articles_updated_at
    BEFORE UPDATE ON articles FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_sources_updated_at
    BEFORE UPDATE ON sources FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION set_updated_at();