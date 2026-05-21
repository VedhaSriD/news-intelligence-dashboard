"""
app/main.py
FastAPI application entry point.
Registers all routers, middleware, CORS, and the APScheduler.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from app.core.config import get_settings
from app.core.logger import setup_logging, get_logger
from app.middleware.rate_limit import RateLimitMiddleware
from app.api.routes_articles   import router as articles_router
from app.api.routes_categories  import router as categories_router
from app.api.routes_sources     import router as sources_router
from app.api.routes_bookmarks   import router as bookmarks_router
from app.api.routes_health      import router as health_router
from app.api.routes_admin       import router as admin_router
from app.jobs.refresh_news      import run_refresh_job
from app.jobs.digest_job        import run_digest_job

setup_logging("INFO")
logger   = get_logger(__name__)
settings = get_settings()
scheduler= AsyncIOScheduler(timezone="UTC")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting scheduler — refresh every {settings.refresh_interval_hours}h")
    scheduler.add_job(
        run_refresh_job,
        trigger=IntervalTrigger(hours=settings.refresh_interval_hours),
        id="news_refresh", replace_existing=True, misfire_grace_time=300,
    )
    scheduler.add_job(
        run_digest_job,
        trigger=CronTrigger(hour=8, minute=0),
        id="daily_digest", replace_existing=True, misfire_grace_time=600,
    )
    scheduler.start()
    logger.info("NewsIntel API v1.0.0 started ✓")
    yield
    scheduler.shutdown()


app = FastAPI(
    title="NewsIntel API",
    description="Verified, deduplicated, categorized global news.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(articles_router)
app.include_router(categories_router)
app.include_router(sources_router)
app.include_router(bookmarks_router)
app.include_router(health_router)
app.include_router(admin_router)


@app.post("/api/v1/jobs/refresh", tags=["system"])
async def manual_refresh(background_tasks: BackgroundTasks):
    """Manually trigger a news refresh. Rate limited to 5/min."""
    background_tasks.add_task(run_refresh_job)
    return {"message": "Refresh job queued", "status": "accepted"}


@app.post("/api/v1/jobs/digest", tags=["system"])
async def manual_digest(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_digest_job)
    return {"message": "Digest job queued", "status": "accepted"}


@app.get("/", tags=["system"])
async def root():
    return {"name": "NewsIntel API", "version": "1.0.0", "docs": "/docs"}