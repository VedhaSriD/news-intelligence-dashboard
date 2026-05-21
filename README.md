# NewsIntel — Global News Intelligence Dashboard

A full-stack news aggregation platform built as a serious engineering portfolio project.  
NewsIntel fetches, deduplicates, scores, and presents global news through a clean editorial-style dashboard with categorized feeds, credibility scoring, bookmarks, and a responsive light UI.

> **Current status:** Frontend prototype is complete and fully functional in demo mode.  
> Backend architecture is designed and documented. Pipeline integration is in progress.

![NewsIntel Dashboard](./docs/screenshots/dashboard-preview.png)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Environment Variables](#environment-variables)
- [Deployment](#deployment)
- [Screenshots](#screenshots)
- [Current Status](#current-status)
- [Future Improvements](#future-improvements)
- [API Reference](#api-reference)
- [License](#license)

## Overview

NewsIntel is a global news intelligence dashboard that aggregates news from multiple verified sources, deduplicates overlapping stories, scores them by credibility and freshness, and presents them through a minimal editorial UI.

The goal was to build something genuinely useful and architecturally sound — not just a CRUD app. The project covers frontend engineering, backend system design, data pipeline thinking, and deployment workflow.

### Key design decisions

- **Deduplication first** — the same story covered by multiple outlets appears once, surfacing the most credible version.
- **Credibility scoring** — every article carries a trust signal derived from source-level quality.
- **Freshness decay** — articles are scored with an exponential decay model so the feed surfaces what matters now.
- **Demo mode** — the frontend runs fully on mock data when the backend is offline, making it easy to preview and share.

## Features

### Frontend

| Feature | Description |
|---------|-------------|
| Latest Feed | Freshest verified articles by default |
| Freshness Filter | Switch between last 6h / 24h / 48h |
| Breaking Ticker | Scrolling top ticker for urgent stories |
| Category Bar | AI, Technology, Education, Politics, Business, Startups, World, Sports, Health |
| Featured Article | Top-ranked story shown in a full-width card |
| Article Cards | Cards with credibility badge, freshness, source, and tags |
| Article Drawer | Slide-in detail panel with source cluster info and fact-check state |
| Search | Full-text search across titles and summaries |
| Archive | Browse older verified news by date |
| Bookmarks | Save articles locally; sync to backend when authenticated |
| Sources Page | Ranked source list with credibility scores and article counts |
| Auth Pages | Clerk-based email/password auth UI |
| Demo Mode | Frontend works without a live backend |
| Loading Skeletons | Shimmer placeholders while loading |
| Empty/Error States | Clear fallback UX across pages |
| Responsive Design | Mobile, tablet, and desktop support |

### Backend architecture

| Component | Description |
|-----------|-------------|
| Ingestion | NewsAPI + RSS feed fetching with URL normalization |
| Classification | Keyword-based post-fetch category correction |
| Deduplication | Multi-layer duplicate detection and winner selection |
| Summarization | Extractive summarizer with optional LLM upgrade |
| Credibility Scoring | Source trust scores with ranking formula |
| Freshness Scoring | Exponential decay with 24-hour half-life |
| Fact Check | Optional Google Fact Check Tools API enrichment |
| Scheduler | APScheduler refresh every 6 hours + GitHub Actions backup |
| Telegram Alerts | Breaking news and failure notifications |
| REST API | 12 endpoints for articles, sources, categories, bookmarks, and health |

## Tech Stack

### Frontend

- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- Motion for React
- Clerk

### Backend

- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- APScheduler
- RapidFuzz
- python-jose
- Tenacity

### Infrastructure

- GitHub Actions
- Docker Compose
- Railway / Render
- Vercel

## Architecture

```text
[NewsAPI] + [RSS Feeds]
          |
          v
fetch_news.py -> normalize URLs, strip tracking
          |
          v
classify.py -> keyword-based category correction
          |
          v
deduplicate.py
  - exact URL hash
  - fuzzy headline similarity
  - time-window clustering
  - winner selection via composite score
          |
          v
summarize.py -> extractive summary / optional LLM
          |
          v
credibility.py -> source trust + fact-check enrichment
          |
          v
PostgreSQL -> articles, clusters, sources, bookmarks
          |
          v
FastAPI -> REST API, auth, jobs
          |
          v
Next.js frontend -> editorial dashboard, search, archive, bookmarks
```

### Deduplication formula

```text
composite_score = credibility * 0.5 + freshness * 0.3 + completeness * 0.2
freshness = exp(-age_hours * ln(2) / 24)
```

The highest-scoring article in each cluster is surfaced in the main feed. Related coverage is stored and shown as supporting sources.

## Project Structure

```text
global-news-intelligence-dashboard/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── (auth)/
│   │   │   │   ├── sign-in/page.tsx
│   │   │   │   └── sign-up/page.tsx
│   │   │   ├── archive/page.tsx
│   │   │   ├── bookmarks/page.tsx
│   │   │   ├── category/[slug]/page.tsx
│   │   │   ├── search/page.tsx
│   │   │   └── sources/page.tsx
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── styles/
│   │   └── types/
│   ├── package.json
│   ├── tailwind.config.ts
│   └── .env.example
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── jobs/
│   │   └── middleware/
│   ├── tests/
│   │   ├── __init__.py
│   │   └── conftest.py
│   ├── requirements.txt
│   └── .env.example
├── database/
│   ├── schema.sql
│   ├── indexes.sql
│   └── seed_sources.sql
├── .github/
│   └── workflows/
│       └── news-refresh.yml
├── docs/
│   ├── architecture.md
│   ├── api-spec.md
│   ├── setup.md
│   └── prompting-guide.md
├── docker-compose.yml
├── README.md
├── .gitignore
└── .env.example
```

## Setup Instructions

### Prerequisites

- Node.js 20+
- Python 3.11+
- PostgreSQL 14+
- [NewsAPI key](https://newsapi.org)
- [Clerk account](https://clerk.com)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/global-news-intelligence-dashboard.git
cd global-news-intelligence-dashboard
```

### 2. Set up the database

```bash
createdb news_intel
psql news_intel < database/schema.sql
psql news_intel < database/indexes.sql
psql news_intel < database/seed_sources.sql
```

### 3. Run the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
```

Set these variables in `backend/.env`:
- `DATABASE_URL`
- `NEWSAPI_KEY`
- `CLERK_SECRET_KEY`

Then start the API:

```bash
uvicorn app.main:app --reload --port 8000
```

Docs will be available at: `http://localhost:8000/docs`

Trigger the first refresh:

```bash
curl -X POST http://localhost:8000/api/v1/jobs/refresh
```

### 4. Run the frontend

```bash
cd frontend
npm install
cp .env.example .env.local
```

Set these variables in `frontend/.env.local`:
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
- `NEXT_PUBLIC_API_URL=http://localhost:8000`

Start the app:

```bash
npm run dev
```

Frontend runs at: `http://localhost:3000`

If the backend is unavailable, the frontend falls back to mock data and shows a Demo Mode indicator.

### 5. Docker

```bash
cp backend/.env.example backend/.env
docker compose up --build
```

Run the frontend separately with `npm run dev`.

## Environment Variables

| Variable | Required | Location |
|----------|----------|----------|
| `DATABASE_URL` | Yes | `backend/.env` |
| `NEWSAPI_KEY` | Yes | `backend/.env` |
| `CLERK_SECRET_KEY` | Yes | `backend/.env` |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Yes | `frontend/.env.local` |
| `NEXT_PUBLIC_API_URL` | Yes | `frontend/.env.local` |
| `GOOGLE_FACTCHECK_API_KEY` | No | `backend/.env` |
| `OPENAI_API_KEY` | No | `backend/.env` |
| `TELEGRAM_BOT_TOKEN` | No | `backend/.env` |

## Deployment

### Frontend on Vercel

```bash
cd frontend
npx vercel
```

Set these environment variables in Vercel:
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
- `NEXT_PUBLIC_API_URL`

### Backend on Railway or Render

Deploy the `backend/` service and provision PostgreSQL. Then set all required backend environment variables in the deployment dashboard.

### Scheduler on GitHub Actions

The workflow at `.github/workflows/news-refresh.yml` runs every 6 hours.

Setup:
1. Push the repository to GitHub.
2. Go to **Settings -> Secrets and variables -> Actions**.
3. Add `BACKEND_URL` with your deployed backend URL.
4. Optionally add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.

## Screenshots

Add screenshots inside `docs/screenshots/` and reference them here.

- Homepage
- Article detail drawer
- Category feed
- Archive page
- Sources page

## Current Status

| Area | Status |
|------|--------|
| Frontend prototype | Complete |
| Demo mode with mock data | Working |
| Auth pages (Clerk) | Integrated |
| Bookmarks (local/demo state) | Working |
| Database schema | Complete |
| Backend API endpoints | Designed and coded |
| News ingestion service | Coded, pending live API-key testing |
| Deduplication pipeline | Coded with unit tests |
| Classifier service | Coded with unit tests |
| Summarization service | Coded |
| Scheduler (APScheduler) | Wired into FastAPI |
| GitHub Actions cron | Configured |
| Frontend-backend integration | In progress |
| Live deployment | Planned |

## Future Improvements

- [ ] Complete frontend-backend integration with live NewsAPI data
- [ ] Add GDELT integration for broader international coverage
- [ ] Add user preference system
- [ ] Add email digest subscription
- [ ] Add Telegram daily digest bot
- [ ] Upgrade search with PostgreSQL full-text search
- [ ] Build admin dashboard for fetch-run monitoring
- [ ] Add CSV / JSON export
- [ ] Add dark mode
- [ ] Add sentiment analysis
- [ ] Add related-articles recommendation
- [ ] Add PWA support

## API Reference

Full API spec: [docs/api-spec.md](./docs/api-spec.md)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/articles/latest` | Latest feed with freshness filter |
| GET | `/api/v1/articles/archive` | Archive by date |
| GET | `/api/v1/articles/{id}` | Single article detail |
| GET | `/api/v1/articles/search` | Full-text search |
| GET | `/api/v1/categories` | Category list with counts |
| GET | `/api/v1/categories/{slug}/articles` | Category feed |
| GET | `/api/v1/sources` | Source list with credibility scores |
| GET | `/api/v1/bookmarks` | User bookmarks |
| POST | `/api/v1/bookmarks` | Save bookmark |
| DELETE | `/api/v1/bookmarks/{id}` | Remove bookmark |
| POST | `/api/v1/jobs/refresh` | Trigger manual news refresh |
| GET | `/api/v1/health` | Health check |

## License

MIT License.

## Author

Built as a serious full-stack engineering portfolio project by Vedha Sree Dumpati.

NewsIntel is designed to make global news easier to read, compare, and trust.
