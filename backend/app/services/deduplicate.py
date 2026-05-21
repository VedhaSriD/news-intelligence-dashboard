"""
services/deduplicate.py
4-layer deduplication + credibility scoring pipeline.

Layer 1: Exact URL hash match
Layer 2+3: Fuzzy headline similarity + time window clustering
Layer 4: Winner selection by composite score
"""
import logging
import re
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from uuid import uuid4

import numpy as np
from rapidfuzz import fuzz

logger = logging.getLogger(__name__)

NEAR_DUPE_THRESHOLD   = 0.88
TIME_WINDOW_HOURS     = 18

SOURCE_CREDIBILITY = {
    "reuters": 0.96, "associated press": 0.95, "ap news": 0.95,
    "bbc news": 0.95, "bbc": 0.92, "the guardian": 0.88,
    "bloomberg": 0.90, "financial times": 0.91, "al jazeera": 0.82,
    "techcrunch": 0.85, "wired": 0.87, "ars technica": 0.88,
    "mit technology review": 0.92, "the verge": 0.84,
    "espn": 0.85, "bbc sport": 0.90, "npr": 0.90,
}


def get_credibility(source_name: str) -> float:
    name = (source_name or "").lower()
    for key, score in SOURCE_CREDIBILITY.items():
        if key in name:
            return score
    return 0.65


def compute_freshness(published_at: datetime) -> float:
    now = datetime.now(timezone.utc)
    if published_at.tzinfo is None:
        published_at = published_at.replace(tzinfo=timezone.utc)
    age_hours = (now - published_at).total_seconds() / 3600
    return max(0.0, float(np.exp(-age_hours * np.log(2) / 24)))


def compute_completeness(article: dict) -> float:
    score = 0.3
    snippet = article.get("content_snippet") or ""
    if len(snippet) > 200: score += 0.3
    if len(snippet) > 400: score += 0.2
    if article.get("image_url"): score += 0.1
    if article.get("author"):    score += 0.1
    return min(1.0, score)


def composite_score(article: dict) -> float:
    c = article.get("credibility_score", 0.65)
    f = article.get("freshness_score",   0.50)
    k = article.get("content_completeness", 0.50)
    return round(c * 0.5 + f * 0.3 + k * 0.2, 4)


def enrich_scores(articles: list[dict]) -> list[dict]:
    for a in articles:
        a["credibility_score"]    = get_credibility(a.get("source_name", ""))
        a["freshness_score"]      = compute_freshness(a["published_at"])
        a["content_completeness"] = compute_completeness(a)
    return articles


def remove_exact_duplicates(articles: list[dict], known: set[str]) -> tuple[list[dict], set[str]]:
    seen, unique, dupes = set(known), [], 0
    for a in articles:
        h = a.get("url_hash")
        if h and h not in seen:
            seen.add(h); unique.append(a)
        else:
            dupes += 1
    logger.info(f"Layer 1: removed {dupes} exact duplicates, {len(unique)} remain")
    return unique, seen


def build_clusters(articles: list[dict]) -> list[list[dict]]:
    clusters: list[list[dict]] = []
    reps:     list[dict]       = []
    sorted_  = sorted(articles, key=lambda x: x["published_at"], reverse=True)

    for article in sorted_:
        title    = article.get("title_normalized") or article.get("title", "")
        pub_time = article["published_at"]
        if pub_time.tzinfo is None:
            pub_time = pub_time.replace(tzinfo=timezone.utc)

        matched = None
        for i, rep in enumerate(reps):
            rep_time = rep["published_at"]
            if rep_time.tzinfo is None:
                rep_time = rep_time.replace(tzinfo=timezone.utc)
            if abs((pub_time - rep_time).total_seconds()) / 3600 > TIME_WINDOW_HOURS:
                continue
            rep_title = rep.get("title_normalized") or rep.get("title", "")
            if fuzz.token_sort_ratio(title, rep_title) / 100.0 >= NEAR_DUPE_THRESHOLD:
                matched = i; break

        if matched is not None:
            clusters[matched].append(article)
        else:
            clusters.append([article]); reps.append(article)

    logger.info(f"Layer 2+3: {len(sorted_)} articles → {len(clusters)} clusters")
    return clusters


def select_winners(clusters: list[list[dict]]) -> list[dict]:
    all_articles = []
    for cluster in clusters:
        cid    = str(uuid4())
        ranked = sorted(cluster, key=composite_score, reverse=True)
        winner = ranked[0]
        for a in cluster:
            a["duplicate_cluster_id"]      = cid
            a["is_cluster_representative"] = (a is winner)
            a["cluster_source_count"]      = len(cluster)
        all_articles.extend(cluster)
    return all_articles


def deduplicate_pipeline(
    articles: list[dict], known_hashes: set[str]
) -> tuple[list[dict], dict]:
    total_raw  = len(articles)
    articles   = enrich_scores(articles)
    articles, _= remove_exact_duplicates(articles, known_hashes)
    after_exact= len(articles)
    clusters   = build_clusters(articles)
    processed  = select_winners(clusters)
    winners    = sum(1 for a in processed if a["is_cluster_representative"])

    stats = {
        "total_raw":        total_raw,
        "after_exact_dedup":after_exact,
        "clusters_formed":  len(clusters),
        "winners":          winners,
        "deduplicated":     total_raw - winners,
    }
    logger.info(f"Dedup stats: {stats}")
    return processed, stats