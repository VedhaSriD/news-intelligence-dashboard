"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import type { Article, CategorySlug, FreshnessWindow } from "@/types";
import { fetchLatestWithFallback } from "@/lib/api";

interface Options {
  category?: CategorySlug | null;
  hours?:    FreshnessWindow;
  enabled?:  boolean;
}

interface Result {
  articles:    Article[];
  loading:     boolean;
  error:       string | null;
  isDemo:      boolean;
  refetch:     () => void;
}

export function useArticles({ category, hours = 6, enabled = true }: Options = {}): Result {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading,  setLoading]  = useState(true);
  const [error,    setError]    = useState<string | null>(null);
  const [isDemo,   setIsDemo]   = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  const fetch_ = useCallback(async () => {
    if (!enabled) return;
    abortRef.current?.abort();
    abortRef.current = new AbortController();
    setLoading(true);
    setError(null);
    try {
      const { articles: data, isDemo: demo } = await fetchLatestWithFallback(hours, category);
      setArticles(data);
      setIsDemo(demo);
    } catch (e: unknown) {
      if ((e as Error)?.name === "AbortError") return;
      setError("Failed to load articles. Please try again.");
    } finally {
      setLoading(false);
    }
  }, [enabled, category, hours]);

  useEffect(() => { fetch_(); }, [fetch_]);

  return { articles, loading, error, isDemo, refetch: fetch_ };
}