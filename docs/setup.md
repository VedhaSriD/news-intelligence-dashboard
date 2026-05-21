# Setup Guide — NewsIntel

## Prerequisites

- Node.js 20+
- Python 3.11+
- PostgreSQL 14+
- A free [Clerk](https://clerk.com) account
- A free [NewsAPI](https://newsapi.org) key

---

## 1. Clone and structure

```bash
git clone https://github.com/yourname/global-news-intelligence-dashboard.git
cd global-news-intelligence-dashboard
```

---

## 2. Database

```bash
createdb news_intel
psql news_intel < database/schema.sql
psql news_intel < database/indexes.sql
psql news_intel < database/seed_sources.sql
```

---

## 3. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env — set DATABASE_URL, NEWSAPI_KEY, CLERK_SECRET_KEY

uvicorn app.main:app --reload --port 8000
```

Swagger docs: http://localhost:8000/docs

Trigger first fetch:
```bash
curl -X POST http://localhost:8000/api/v1/jobs/refresh
```

---

## 4. Frontend

```bash
cd frontend
npm install

cp .env.example .env.local
# Set NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY and CLERK_SECRET_KEY from clerk.com
# Set NEXT_PUBLIC_API_URL=http://localhost:8000

npm run dev
```

Dashboard: http://localhost:3000

> Without a NewsAPI key the frontend runs in **Demo Mode** using mock data automatically.

---

## 5. Scheduler (GitHub Actions)

1. Push project to GitHub
2. Go to **Settings → Secrets → Actions**
3. Add `BACKEND_URL` = your deployed backend URL
4. The workflow in `.github/workflows/news-refresh.yml` runs every 6 hours automatically

---

## 6. Docker (optional)

```bash
docker compose up --build
```

---

## Environment Variables Summary

| Variable | Required | Where |
|----------|----------|-------|
| `DATABASE_URL` | ✓ | backend/.env |
| `NEWSAPI_KEY` | ✓ | backend/.env |
| `CLERK_SECRET_KEY` | ✓ | backend/.env |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | ✓ | frontend/.env.local |
| `NEXT_PUBLIC_API_URL` | ✓ | frontend/.env.local |
| `GOOGLE_FACTCHECK_API_KEY` | optional | backend/.env |
| `OPENAI_API_KEY` | optional | backend/.env |
| `TELEGRAM_BOT_TOKEN` | optional | backend/.env |