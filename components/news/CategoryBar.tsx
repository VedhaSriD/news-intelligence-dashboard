"use client";

import { cn } from "@/lib/utils";
import { CATEGORY_META, ALL_CATEGORIES } from "@/lib/constants";
import type { CategorySlug } from "@/types";

export function CategoryBar({
  selected,
  onSelect,
}: {
  selected:  CategorySlug | null;
  onSelect:  (slug: CategorySlug | null) => void;
}) {
  return (
    <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-0.5">
      <Chip label="All" active={selected === null} onClick={() => onSelect(null)} />
      {ALL_CATEGORIES.map((slug) => (
        <Chip
          key={slug}
          label={CATEGORY_META[slug].label}
          active={selected === slug}
          onClick={() => onSelect(slug === selected ? null : slug)}
        />
      ))}
    </div>
  );
}

function Chip({
  label,
  active,
  onClick,
}: {
  label:   string;
  active:  boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "flex-shrink-0 px-3.5 py-1.5 rounded-full text-[12px] font-medium transition-colors whitespace-nowrap",
        active
          ? "bg-mauve-700 text-white"
          : "bg-mauve-50 text-ink-muted border border-[var(--border)] hover:bg-mauve-100 hover:text-ink-soft"
      )}
    >
      {label}
    </button>
  );
}