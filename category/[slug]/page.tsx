"use client";

import { useState, use } from "react";
import { useArticles } from "@/hooks/useArticles";
import { useBookmarks } from "@/hooks/useBookmarks";
import { useToast } from "@/hooks/useToast";
import { FreshnessFilter } from "@/components/news/FreshnessFilter";
import { ArticleCard } from "@/components/news/ArticleCard";
import { ArticleDrawer } from "@/components/news/ArticleDrawer";
import { SkeletonGrid } from "@/components/skeletons/CardSkeleton";
import { EmptyState } from "@/components/ui/EmptyState";
import { ErrorState } from "@/components/ui/ErrorState";
import { CATEGORY_META } from "@/lib/constants";
import type { Article, CategorySlug, FreshnessWindow } from "@/types";

export default function CategoryPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(params);
  const meta     = CATEGORY_META[slug as CategorySlug];
  const [hours,  setHours]  = useState<FreshnessWindow>(24);
  const [drawer, setDrawer] = useState<Article | null>(null);

  const { toggle, isBookmarked } = useBookmarks();
  const { success }               = useToast();
  const { articles, loading, error, refetch } = useArticles({ category: slug as CategorySlug, hours });

  function handleBookmark(id: string) {
    const was = isBookmarked(id);
    toggle(id);
    success(was ? "Removed from bookmarks" : "Saved to bookmarks");
  }

  if (!meta) {
    return <EmptyState icon="🔍" title="Category not found" description="This category does not exist." />;
  }

  return (
    <>
      <div className="border-b border-[var(--border)] bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="text-3xl">{meta.emoji}</span>
            <div>
              <h1 className="font-display text-2xl font-semibold text-ink">{meta.label}</h1>
              <p className="text-[12px] text-ink-muted mt-0.5">{meta.description}</p>
            </div>
          </div>
          <FreshnessFilter value={hours} onChange={setHours} />
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-4">
        <p className="text-[12px] text-ink-muted">
          {loading ? "Loading…" : `${articles.length} article${articles.length !== 1 ? "s" : ""}`}
        </p>

        {error ? <ErrorState message={error} onRetry={refetch} />
          : loading ? <SkeletonGrid count={6} />
          : articles.length === 0 ? (
            <EmptyState icon={meta.emoji} title={`No ${meta.label} articles`}
              description="Check back after the next refresh." />
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