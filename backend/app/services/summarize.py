"""
services/summarize.py
Extractive summarizer with optional OpenAI upgrade.
Works offline with zero dependencies — just Python.
"""
import re
import logging
from app.core.config import get_settings

logger   = logging.getLogger(__name__)
settings = get_settings()

STOPWORDS = {
    "the","a","an","and","or","but","in","on","at","to","for","of","with",
    "by","from","is","was","are","were","be","been","being","have","has",
    "had","do","does","did","it","its","this","that","these","those","i",
    "we","you","he","she","they","said","according","told","would","could",
}


def extractive_summary(text: str, n: int = 3) -> str:
    if not text or len(text.strip()) < 100:
        return text.strip() if text else ""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if len(s.strip()) > 30]
    if len(sentences) <= n:
        return " ".join(sentences)
    freq: dict[str, int] = {}
    for s in sentences:
        for w in s.lower().split():
            w = re.sub(r"[^a-z]", "", w)
            if w and w not in STOPWORDS:
                freq[w] = freq.get(w, 0) + 1
    scores = [
        (i, sum(freq.get(re.sub(r"[^a-z]", "", w), 0) for w in s.lower().split()) * (1.0 / (1 + i * 0.1)))
        for i, s in enumerate(sentences)
    ]
    top = sorted(sorted(scores, key=lambda x: x[1], reverse=True)[:n], key=lambda x: x[0])
    return " ".join(sentences[i] for i, _ in top)


async def generate_summary(article: dict) -> str:
    text  = article.get("content_snippet") or article.get("summary") or ""
    title = article.get("title", "")
    if not text and not title:
        return ""
    if settings.openai_api_key:
        try:
            return await _openai_summary(title, text)
        except Exception as e:
            logger.warning(f"OpenAI summary failed: {e}")
    return extractive_summary(f"{title}. {text}" if title not in text else text)


async def _openai_summary(title: str, content: str) -> str:
    import httpx
    prompt = (
        f"Summarize this news article in 3-4 concise sentences. "
        f"Focus on key facts, who is involved, and why it matters. "
        f"Do not use 'The article says' or 'According to'.\n\n"
        f"Title: {title}\n\nContent: {content[:1000]}"
    )
    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.openai_api_key}"},
            json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": 150, "temperature": 0.3},
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()


async def batch_summarize(articles: list[dict]) -> list[dict]:
    for a in articles:
        if not a.get("summary"):
            a["summary"] = await generate_summary(a)
    return articles