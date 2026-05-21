"use client";

import { useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";

import { cn, timeAgo, formatScore } from "@/lib/utils";
import { Badge, FactBadge } from "@/components/ui/Badge";
import { CATEGORY_META } from "@/lib/constants";

import type { Article, CategorySlug } from "@/types";

type Props = {
  article: Article | null;
  isBookmarked: boolean;
  onClose: () => void;
  onBookmark: (id: string) => void;
};

export function ArticleDrawer({
  article,
  isBookmarked,
  onClose,
  onBookmark,
}: Props) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };

    window.addEventListener("keydown", handler);

    return () => {
      window.removeEventListener("keydown", handler);
    };
  }, [onClose]);

  useEffect(() => {
    document.body.style.overflow = article ? "hidden" : "";

    return () => {
      document.body.style.overflow = "";
    };
  }, [article]);

  const cat = article
    ? CATEGORY_META[article.category as CategorySlug]
    : null;

  return (
    <AnimatePresence>
      {article && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 z-40 bg-black/20 backdrop-blur-sm"
            onClick={onClose}
          />

          <motion.aside
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{
              type: "spring",
              damping: 30,
              stiffness: 300,
            }}
            className="fixed top-0 right-0 bottom-0 z-50 w-full max-w-[420px] overflow-y-auto border-l border-zinc-200 bg-white shadow-2xl"
          >
            <div className="flex items-center justify-between border-b border-zinc-200 px-5 py-4">
              <h2 className="text-sm font-semibold text-zinc-700">
                Article Details
              </h2>

              <button
                onClick={onClose}
                className="rounded-lg p-2 transition hover:bg-zinc-100"
              >
                ✕
              </button>
            </div>

            <div className="space-y-5 p-5">
              {article.is_breaking && (
                <div className="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-xs font-semibold text-red-700">
                  Breaking News
                </div>
              )}

              <div className="space-y-3">
                <Badge variant="category">
                  {cat?.label || article.category}
                </Badge>

                <h1 className="text-xl font-semibold leading-snug text-zinc-900">
                  {article.title}
                </h1>

                <div className="flex flex-wrap items-center gap-2 text-xs text-zinc-500">
                  <span>{article.source_name}</span>
                  <span>•</span>
                  <span>{timeAgo(article.published_at)}</span>
                </div>
              </div>

              {article.summary && (
                <div className="rounded-2xl border border-zinc-200 bg-zinc-50 p-4">
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-zinc-500">
                    Summary
                  </p>

                  <p className="text-sm leading-relaxed text-zinc-700">
                    {article.summary}
                  </p>
                </div>
              )}

              <div className="grid grid-cols-2 gap-3">
                <div className="rounded-2xl border border-zinc-200 p-4">
                  <p className="text-xs text-zinc-500">Credibility</p>

                  <p className="mt-1 text-2xl font-semibold">
                    {formatScore(article.credibility_score)}
                  </p>
                </div>

                <div className="rounded-2xl border border-zinc-200 p-4">
                  <p className="text-xs text-zinc-500">Freshness</p>

                  <p className="mt-1 text-2xl font-semibold">
                    {formatScore(article.freshness_score)}
                  </p>
                </div>
              </div>

              {article.tags?.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {article.tags.map((tag) => (
                    <span
                      key={tag}
                      className="rounded-full bg-zinc-100 px-3 py-1 text-xs text-zinc-600"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              )}

              <FactBadge status={article.fact_check_status} />

              <button
                onClick={() => onBookmark(article.id)}
                className={cn(
                  "w-full rounded-xl border px-4 py-3 text-sm font-medium transition",
                  isBookmarked
                    ? "border-mauve-300 bg-mauve-50 text-mauve-700"
                    : "border-zinc-200 hover:bg-zinc-50"
                )}
              >
                {isBookmarked
                  ? "Saved to Bookmarks"
                  : "Save to Bookmarks"}
              </button>

              {article.canonical_url && (
                <a
                  href={article.canonical_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex w-full items-center justify-center rounded-xl bg-[#3e1d32] px-4 py-3 text-sm font-medium text-white transition hover:opacity-90"
                >
                  Read Full Article
                </a>
              )}
            </div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}