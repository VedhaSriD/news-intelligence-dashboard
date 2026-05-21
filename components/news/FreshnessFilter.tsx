"use client";

import { cn } from "@/lib/utils";
import { FRESHNESS_OPTIONS } from "@/lib/constants";
import type { FreshnessWindow } from "@/types";

export function FreshnessFilter({
  value,
  onChange,
}: {
  value:    FreshnessWindow;
  onChange: (v: FreshnessWindow) => void;
}) {
  return (
    <div className="flex items-center gap-0.5 bg-mauve-50 border border-[var(--border)] rounded-full p-0.5">
      {FRESHNESS_OPTIONS.map((opt) => (
        <button
          key={opt.value}
          onClick={() => onChange(opt.value)}
          className={cn(
            "px-3 py-1 rounded-full text-[12px] font-medium transition-all whitespace-nowrap",
            value === opt.value
              ? "bg-white text-mauve-700 shadow-sm"
              : "text-ink-muted hover:text-ink-soft"
          )}
        >
          {opt.label}
        </button>
      ))}
    </div>
  );
}