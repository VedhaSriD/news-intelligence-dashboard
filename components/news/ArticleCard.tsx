"use client";

import { motion } from "motion/react";
import { cn, timeAgo } from "@/lib/utils";
import { Badge, CredBadge } from "@/components/ui/Badge";
import { CATEGORY_META } from "@/lib/constants";
import type { Article, CategorySlug } from "@/types";

export function ArticleCard({
  article,
  index = 0,
  isBookmarked,
  onOpen,
  onBookmark,
}: {
  article:      Article;
  index?:       number;
  isBookmarked: boolean;
  onOpen:       (a: Article) => void;
  onBookmark:   (id: string) => void;
}) {
  const cat = CATEGORY_META[article.category as CategorySlug];

  return (
    <motion.article
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.05, ease: [0.22, 1, 0.36, 1] }}
      whileHover={{ y: -3, transition: { duration: 0.18 } }}
      onClick={() => onOpen(article)}
      className="group bg-white border border-[var(--border)] rounded-2xl p-4 cursor-pointer flex flex-col gap-3 hover:shadow-hover hover:border-[var(--border-md)] transition-shadow duration-200"
    >
      {/* Top row */}
      <div className="flex items-start justify-between gap-2">
        <div className="flex flex-wrap gap-1.5">
          {article.is_breaking && <Badge variant="breaking">● Breaking</Badge>}
          <Badge variant="category">{cat?.label ?? article.category}</Badge>
        </div>
        <div className="flex items-center gap-1.5 flex-shrink-0">
          <span className="text-[11px] text-ink-faint whitespace-nowrap">
            {timeAgo(article.published_at)}
          </span>
          <button
            onClick={(e) => { e.stopPropagation(); onBookmark(article.id); }}
            aria-label={isBookmarked ? "Remove bookmark" : "Save article"}
            className={cn(
              "w-6 h-6 rounded-md flex items-center justify-center transition-colors",
              isBookmarked
                ? "text-mauve-600 bg-mauve-50"
                : "text-ink-faint hover:text-mauve-500 hover:bg-mauve-50"
            )}
          >
            <BookmarkIcon filled={isBookmarked} />
          </button>
        </div>
      </div>

      {/* Title */}
      <h3 className="font-display text-[14px] font-semibold leading-snug text-ink line-clamp-3 group-hover:text-mauve-700 transition-colors">
        {article.title}
      </h3>

      {/* Summary */}
      {article.summary && (
        <p className="text-[12px] text-ink-muted leading-relaxed line-clamp-2">
          {article.summary}
        </p>
      )}

      {/* Credibility */}
      <CredBadge score={article.credibility_score} />

      {/* Footer */}
      <div className="flex items-center justify-between pt-2.5 border-t border-[var(--border)] mt-auto">
        <div className="flex items-center gap-1.5">
          <div className="w-4 h-4 rounded bg-mauve-100 flex items-center justify-center text-[8px] font-bold text-mauve-700 flex-shrink-0">
            {article.source_name.charAt(0)}
          </div>
          <span className="text-[11px] text-ink-muted truncate max-w-[110px]">
            {article.source_name}
          </span>
        </div>
        <span className="text-[11px] font-medium text-mauve-600 group-hover:text-mauve-700 transition-colors">
          Read →
        </span>
      </div>
    </motion.article>
  );
}

function BookmarkIcon({ filled }: { filled: boolean }) {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24"
      fill={filled ? "currentColor" : "none"}
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
    >
      <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" />
    </svg>
  );
}