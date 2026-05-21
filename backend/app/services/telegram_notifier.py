"""
services/telegram_notifier.py
Sends breaking alerts and daily digests to a Telegram chat.
All methods are no-ops when TELEGRAM_BOT_TOKEN is not set.
"""
import logging
from datetime import datetime, timezone
import httpx
from tenacity import retry, stop_after_attempt, wait_fixed
from app.core.config import get_settings

logger   = logging.getLogger(__name__)
settings = get_settings()

CATEGORY_EMOJI = {
    "ai": "🤖", "technology": "💻", "education": "📚", "politics": "🏛️",
    "business": "📈", "startups": "🚀", "world": "🌍", "sports": "⚽", "health": "🏥",
}


def _bot_url(method: str) -> str:
    return f"https://api.telegram.org/bot{settings.telegram_bot_token}/{method}"


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def send_message(text: str) -> bool:
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        return False
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(_bot_url("sendMessage"), json={
                "chat_id": settings.telegram_chat_id,
                "text": text, "parse_mode": "HTML",
                "disable_web_page_preview": False,
            })
            return resp.status_code == 200
    except Exception as e:
        logger.error(f"Telegram send failed: {e}")
        return False


async def send_breaking_alert(article: dict) -> bool:
    emoji = CATEGORY_EMOJI.get(article.get("category", ""), "📰")
    text  = (
        f"🔴 <b>BREAKING NEWS</b>\n\n"
        f"{emoji} <b>{article.get('title', '')}</b>\n\n"
        f"{(article.get('summary') or '')[:300]}\n\n"
        f"📡 <i>{article.get('source_name', '')}</i>"
    )
    return await send_message(text)


async def send_daily_digest(articles: list[dict], top_n: int = 10) -> bool:
    if not articles:
        return False
    date = datetime.now(timezone.utc).strftime("%A, %d %b %Y")
    lines= [f"📰 <b>News Digest — {date}</b>\n"]
    for i, a in enumerate(articles[:top_n], 1):
        emoji = CATEGORY_EMOJI.get(a.get("category", ""), "📰")
        url   = a.get("canonical_url") or "#"
        lines.append(f"{i}. {emoji} <a href='{url}'>{a.get('title','')}</a>")
    text = "\n".join(lines)
    if len(text) > 4000:
        text = text[:3990] + "\n..."
    return await send_message(text)


async def send_refresh_summary(stats: dict) -> bool:
    text = (
        f"✅ <b>News Refresh Complete</b>\n\n"
        f"📥 Fetched: {stats.get('total_raw', 0)}\n"
        f"🔁 Deduplicated: {stats.get('deduplicated', 0)}\n"
        f"💾 Saved: {stats.get('inserted', 0)}\n"
        f"🕐 {datetime.now(timezone.utc).strftime('%H:%M UTC')}"
    )
    return await send_message(text)