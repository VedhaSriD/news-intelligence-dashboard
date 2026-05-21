"use client";

import { useState, useCallback, useEffect } from "react";

const KEY = "ni_bookmarks";

export function useBookmarks() {
  const [bookmarks, setBookmarks] = useState<Set<string>>(new Set());

  useEffect(() => {
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) setBookmarks(new Set(JSON.parse(raw) as string[]));
    } catch { /* ignore */ }
  }, []);

  const persist = useCallback((next: Set<string>) => {
    setBookmarks(next);
    try { localStorage.setItem(KEY, JSON.stringify([...next])); } catch { /* ignore */ }
  }, []);

  const toggle = useCallback((id: string) => {
    const next = new Set(bookmarks);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    persist(next);
  }, [bookmarks, persist]);

  const isBookmarked = useCallback((id: string) => bookmarks.has(id), [bookmarks]);

  return { bookmarks, toggle, isBookmarked };
}