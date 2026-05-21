"use client";

import { useState } from "react";
import { format, subDays, parseISO } from "date-fns";
import { ArticleCard } from "@/components/news/ArticleCard";
import { ArticleDrawer } from "@/components/news/ArticleDrawer";
import { SkeletonGrid } from "@/components/skeletons/CardSkeleton";
import { EmptyState } from "@/components/ui/EmptyState";
import { useBookmarks } from "@/hooks/useBookmarks";
import { useToast } from "@/hooks/useToast";
import { MOCK_ARTICLES } from "@/lib/constants";
import type { Article } from "@/types";

const TODAY = new Date();

const QUICK = [
  { label: "Yesterday",  days: 1 },
  { label: "2 days ago", days: 2 },
  { label: "3 days ago", days: 3 },
  { label: "Last week",  days: 7 },
];

export default function ArchivePage() {
  const [selected, setSelected] = useState(format(subDays(TODAY, 1), "yyyy-MM-dd"));
  const [loading,  setLoading]  = useState(false);
  const [drawer,   setDrawer]   = useState<Article | null>(null);

  const { toggle, isBookmarked } = useBookmarks();
  const { success }               = useToast();

  // MOCK — replace with articlesApi.archive({ date: selected }) when backend is ready
  const articles = MOCK_ARTICLES as Article[];

  function pick(dateStr: string) {
    setLoading(true);
    setSelected(dateStr);
    setTimeout(() => setLoading(false), 500);
  }

  function handleBookmark(id: string) {
    const was = isBookmarked(id);
    toggle(id);
    success(was ? "Removed from bookmarks" : "Saved to bookmarks");
  }

  return (
    <>
      <div className="border-b border-[var(--border)] bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="font-display text-2xl font-semibold text-ink mb-1">News Archive</h1>
          <p className="text-[12px] text-ink-muted mb-5">Browse verified news from any past date</p>
          <div className="flex flex-wrap gap-2 items-center">
            {QUICK.map(({ label, days }) => {
              const ds     = format(subDays(TODAY, days), "yyyy-MM-dd");
              const active = selected === ds;
              return (
                <button key={days} onClick={() => pick(ds)}
                  className={`px-3.5 py-1.5 rounded-full text-[12px] font-medium transition-colors ${
                    active
                      ? "bg-mauve-700 text-white"
                      : "bg-mauve-50 border border-[var(--border)] text-ink-muted hover:bg-mauve-100"
                  }`}>
                  {label}
                  <span className="ml-1.5 text-[10px] opacity-60">{format(subDays(TODAY, days), "MMM d")}</span>
                </button>
              );
            })}
            <input type="date" value={selected}
              max={format(subDays(TODAY, 1), "yyyy-MM-dd")}
              min={format(subDays(TODAY, 30), "yyyy-MM-dd")}
              onChange={(e) => pick(e.target.value)}
              className="px-3 py-1.5 rounded-full text-[12px] border border-[var(--border-md)] text-ink-muted bg-white focus:outline-none focus:ring-2 focus:ring-mauve-200"
            />
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-4">
        <div className="flex items-center justify-between">
          <p className="font-display text-base font-semibold text-ink">
            {format(parseISO(selected), "EEEE, MMMM d, yyyy")}
          </p>
          <p className="text-[12px] text-ink-muted">
            {loading ? "Loading…" : `${articles.length} articles`}
          </p>
        </div>

        {loading ? <SkeletonGrid count={6} /> : articles.length === 0 ? (
          <EmptyState icon="🗓️" title="No articles for this date" description="The archive goes back 30 days." />
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {articles.map((a, i) => (
              <ArticleCard key={a.id} article={a} index={i}
                isBookmarked={isBookmarked(a.id)} onOpen={setDrawer} onBookmark={handleBookmark} />
            ))}
          </div>
        )}
      </div>

      <ArticleDrawer article={drawer}
        isBookmarked={drawer ? isBookmarked(drawer.id) : false}
        onClose={() => setDrawer(null)} onBookmark={handleBookmark} />
    </>
  );
}