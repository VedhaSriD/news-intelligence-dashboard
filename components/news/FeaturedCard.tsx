"use client";

import { motion } from "motion/react";
import { cn, timeAgo, formatScore } from "@/lib/utils";
import { Badge, CredBadge, FactBadge } from "@/components/ui/Badge";
import { CATEGORY_META } from "@/lib/constants";
import type { Article, CategorySlug } from "@/types";

export function FeaturedCard({
  article,
  isBookmarked,
  onOpen,
  onBookmark,
}: {
  article:      Article;
  isBookmarked: boolean;
  onOpen:       (a: Article) => void;
  onBookmark:   (id: string) => void;
}) {
  const cat = CATEGORY_META[article.category as CategorySlug];

  return (
    <motion.article
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
      whileHover={{ y: -2, transition: { duration: 0.18 } }}
      onClick={() => onOpen(article)}
      className="col-span-full group bg-white border border-[var(--border)] rounded-2xl overflow-hidden cursor-pointer hover:shadow-hover hover:border-[var(--border-md)] transition-shadow duration-200"
    >
      <div className="h-0.5 bg-mauve-500" />

      <div className="p-5 md:p-6 flex flex-col md:flex-row gap-6">
        {/* Left */}
        <div className="flex-1 min-w-0">
          <div className="flex flex-wrap items-center gap-2 mb-3">
            {article.is_breaking && <Badge variant="breaking">● Breaking</Badge>}
            <Badge variant="category">{cat?.label ?? article.category}</Badge>
            <CredBadge score={article.credibility_score} />
            <span className="text-[11px] text-ink-faint ml-auto">
              {timeAgo(article.published_at)}
            </span>
            <button
              onClick={(e) => { e.stopPropagation(); onBookmark(article.id); }}
              aria-label={isBookmarked ? "Remove bookmark" : "Save"}
              className={cn(
                "w-6 h-6 rounded-md flex items-center justify-center transition-colors",
                isBookmarked
                  ? "text-mauve-600 bg-mauve-50"
                  : "text-ink-faint hover:text-mauve-500 hover:bg-mauve-50"
              )}
            >
              <svg width="13" height="13" viewBox="0 0 24 24"
                fill={isBookmarked ? "currentColor" : "none"}
                stroke="currentColor" strokeWidth="2"
                strokeLinecap="round" strokeLinejoin="round"
              >
                <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" />
              </svg>
            </button>
          </div>

          <h2 className="font-display text-xl md:text-2xl font-semibold text-ink leading-snug mb-2 group-hover:text-mauve-700 transition-colors">
            {article.title}
          </h2>

          {article.summary && (
            <p className="text-[13px] text-ink-muted leading-relaxed line-clamp-3 mb-4">
              {article.summary}
            </p>
          )}

          {article.tags.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mb-4">
              {article.tags.slice(0, 5).map((tag) => (
                <span key={tag}
                  className="px-2 py-0.5 bg-mauve-50 text-mauve-600 text-[10px] rounded-full border border-mauve-100">
                  #{tag}
                </span>
              ))}
            </div>
          )}

          <div className="flex items-center justify-between pt-3 border-t border-[var(--border)]">
            <div className="flex items-center gap-2">
              <div className="w-5 h-5 rounded bg-mauve-100 flex items-center justify-center text-[9px] font-bold text-mauve-700">
                {article.source_name.charAt(0)}
              </div>
              <span className="text-[12px] font-medium text-ink-soft">{article.source_name}</span>
              {article.author && (
                <span className="text-[12px] text-ink-muted">· {article.author}</span>
              )}
            </div>
            <span className="text-[12px] font-medium text-mauve-600 group-hover:text-mauve-700">
              Read full story →
            </span>
          </div>
        </div>

        {/* Right: intel panel */}
        <div className="flex-shrink-0 w-full md:w-44 bg-mauve-50 border border-mauve-100 rounded-xl p-4">
          <p className="text-[10px] font-semibold text-mauve-600 uppercase tracking-wider mb-3">
            Source intel
          </p>
          {[
            { label: "Credibility", value: article.credibility_score },
            { label: "Freshness",   value: article.freshness_score   },
          ].map(({ label, value }) => (
            <div key={label} className="mb-2.5">
              <div className="flex justify-between text-[10px] text-ink-muted mb-1">
                <span>{label}</span>
                <span className="font-medium">{formatScore(value)}</span>
              </div>
              <div className="h-1 bg-mauve-200 rounded-full overflow-hidden">
                <div className="h-full bg-mauve-500 rounded-full" style={{ width: `${value * 100}%` }} />
              </div>
            </div>
          ))}
          <div className="pt-2.5 border-t border-mauve-200 mt-1">
            <p className="text-[10px] text-ink-muted mb-1">Coverage</p>
            <p className="text-[11px] font-medium text-ink">{article.cluster_source_count} sources</p>
          </div>
          <div className="pt-2.5 border-t border-mauve-200 mt-2.5">
            <FactBadge status={article.fact_check_status} />
          </div>
        </div>
      </div>
    </motion.article>
  );
}