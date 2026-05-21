"use client";

import { useState } from "react";
import { SignedIn, SignedOut } from "@clerk/nextjs";
import Link from "next/link";
import { ArticleCard } from "@/components/news/ArticleCard";
import { ArticleDrawer } from "@/components/news/ArticleDrawer";
import { EmptyState } from "@/components/ui/EmptyState";
import { useBookmarks } from "@/hooks/useBookmarks";
import { useToast } from "@/hooks/useToast";
import { MOCK_ARTICLES } from "@/lib/constants";
import type { Article } from "@/types";

/**
 * Bookmarks page.
 * MOCK: Article list is sourced from MOCK_ARTICLES filtered by localStorage bookmark IDs.
 * When backend is ready: replace with bookmarksApi.list(token) call.
 */
export default function BookmarksPage() {
  const [drawer, setDrawer] = useState<Article | null>(null);
  const { toggle, isBookmarked } = useBookmarks();
  const { success }               = useToast();

  const saved = (MOCK_ARTICLES as Article[]).filter((a) => isBookmarked(a.id));

  function handleBookmark(id: string) {
    const was = isBookmarked(id);
    toggle(id);
    success(was ? "Removed from bookmarks" : "Saved to bookmarks");
  }

  return (
    <>
      <div className="border-b border-[var(--border)] bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="font-display text-2xl font-semibold text-ink mb-1">
            Bookmarks
          </h1>
          <p className="text-[12px] text-ink-muted">Your saved articles</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <SignedOut>
          <EmptyState
            icon="🔒"
            title="Sign in to save bookmarks"
            description="Create a free account to save articles and access them across sessions."
            action={
              <Link
                href="/sign-in"
                className="inline-block px-5 py-2.5 rounded-xl bg-mauve-800 text-white text-[13px] font-medium hover:bg-mauve-900 transition-colors"
              >
                Sign in
              </Link>
            }
          />
        </SignedOut>

        <SignedIn>
          {saved.length === 0 ? (
            <EmptyState
              icon="🔖"
              title="No bookmarks yet"
              description="Click the bookmark icon on any article to save it here."
              action={
                <Link
                  href="/"
                  className="inline-block px-5 py-2.5 rounded-xl border border-[var(--border-md)] text-[13px] font-medium text-ink-muted hover:bg-mauve-50 transition-colors"
                >
                  Browse latest news
                </Link>
              }
            />
          ) : (
            <>
              <p className="text-[12px] text-ink-muted mb-5">
                {saved.length} saved article{saved.length !== 1 ? "s" : ""}
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {saved.map((a, i) => (
                  <ArticleCard
                    key={a.id}
                    article={a}
                    index={i}
                    isBookmarked={true}
                    onOpen={setDrawer}
                    onBookmark={handleBookmark}
                  />
                ))}
              </div>
            </>
          )}
        </SignedIn>
      </div>

      <ArticleDrawer
        article={drawer}
        isBookmarked={drawer ? isBookmarked(drawer.id) : false}
        onClose={() => setDrawer(null)}
        onBookmark={handleBookmark}
      />
    </>
  );
}