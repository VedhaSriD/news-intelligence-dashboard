# API Specification — NewsIntel

Base URL: `http://localhost:8000` (dev) | `https://your-api.com` (prod)

All responses: JSON. Timestamps: ISO 8601 UTC.

---

## Articles

### GET /api/v1/articles/latest

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| hours | int | 6 | Time window 1–72h |
| category | string | — | Filter by slug |
| page | int | 1 | Page number |
| page_size | int | 20 | Results per page |

### GET /api/v1/articles/archive

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| date | string | ✓ | YYYY-MM-DD |
| category | string | — | Filter |

### GET /api/v1/articles/search?q=openai

### GET /api/v1/articles/{id}

---

## Categories

### GET /api/v1/categories
Returns all categories with article counts (last 24h).

### GET /api/v1/categories/{slug}/articles

---

## Sources

### GET /api/v1/sources

---

## Bookmarks (requires Clerk JWT)

### GET /api/v1/bookmarks
### POST /api/v1/bookmarks  `{ "article_id": "uuid" }`
### DELETE /api/v1/bookmarks/{article_id}

---

## System

### GET /api/v1/health
### POST /api/v1/jobs/refresh
### POST /api/v1/jobs/digest
### GET /api/v1/admin/stats
### GET /api/v1/admin/fetch-runs

---

## Article Object

```json
{
  "id": "uuid",
  "title": "string",
  "summary": "string | null",
  "category": "ai | technology | education | politics | business | startups | world | sports | health",
  "source_name": "string",
  "canonical_url": "string",
  "published_at": "ISO 8601",
  "credibility_score": 0.00–1.00,
  "freshness_score": 0.00–1.00,
  "composite_score": 0.00–1.00,
  "fact_check_status": "clear | flagged | unchecked",
  "is_breaking": true,
  "cluster_source_count": 5,
  "tags": ["string"]
}
```