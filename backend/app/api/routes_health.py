"""
api/routes_health.py
Health check + system info.
"""
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import get_settings
from app.models.article import FetchRun
from app.schemas.article import HealthResponse

router   = APIRouter(prefix="/api/v1", tags=["system"])
settings = get_settings()


@router.get("/health", response_model=HealthResponse)
async def health(db: AsyncSession = Depends(get_db)):
    db_ok        = False
    latest_fetch = None
    try:
        await db.execute(select(func.now()))
        db_ok = True
        result = (await db.execute(
            select(FetchRun.completed_at)
            .where(FetchRun.status == "success")
            .order_by(desc(FetchRun.completed_at))
            .limit(1)
        )).scalar_one_or_none()
        latest_fetch = result
    except Exception:
        pass

    return HealthResponse(
        status="ok" if db_ok else "degraded",
        env=settings.app_env,
        db_connected=db_ok,
        latest_fetch=latest_fetch,
    )