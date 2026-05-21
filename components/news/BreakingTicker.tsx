"use client";

import { timeAgo } from "@/lib/utils";
import type { Article } from "@/types";

/**
 * Scrolling breaking news ticker.
 * Uses the Tailwind animate-marquee utility defined in tailwind.config.ts.
 * No inline <style> or styled-jsx — avoids the conflict with the Tailwind keyframe.
 */
export function BreakingTicker({
  articles,
  onSelect,
}: {
  articles:  Article[];
  onSelect?: (a: Article) => void;
}) {
  if (articles.length === 0) return null;

  // Duplicate items so the scroll loop is seamless
  const items = [...articles, ...articles];

  return (
    <div className="bg-mauve-900 h-8 flex items-center overflow-hidden select-none">
      {/* Live label */}
      <div className="flex-shrink-0 flex items-center gap-2 px-4 h-full border-r border-mauve-700/60">
        <span className="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse" />
        <span className="text-[10px] font-semibold tracking-widest uppercase text-mauve-300">
          Live
        </span>
      </div>

      {/* Scrolling strip */}
      <div className="flex-1 overflow-hidden">
        <div className="flex items-center whitespace-nowrap animate-marquee">
          {items.map((article, i) => (
            <button
              key={`${article.id}-${i}`}
              onClick={() => onSelect?.(article)}
              className="inline-flex items-center gap-3 px-6 text-[11px] text-mauve-300 hover:text-white transition-colors"
            >
              <span className="font-medium">{article.title}</span>
              <span className="text-mauve-600 text-[10px]">
                {timeAgo(article.published_at)}
              </span>
              <span className="text-mauve-700">·</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}