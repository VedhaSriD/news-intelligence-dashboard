import { cn } from "@/lib/utils";
import { credibilityTier, credibilityLabel } from "@/lib/utils";
import type { FactCheckStatus } from "@/types";

type Variant =
  | "breaking" | "category" | "verified"
  | "trusted"  | "unverified" | "neutral";

const STYLES: Record<Variant, string> = {
  breaking:   "bg-red-50 text-red-700 border border-red-100",
  category:   "bg-mauve-50 text-mauve-700 border border-mauve-100",
  verified:   "bg-emerald-50 text-emerald-700 border border-emerald-100",
  trusted:    "bg-amber-50 text-amber-700 border border-amber-100",
  unverified: "bg-red-50 text-red-700 border border-red-100",
  neutral:    "bg-mauve-50 text-ink-muted border border-[var(--border)]",
};

export function Badge({
  variant,
  children,
  className,
}: {
  variant:   Variant;
  children:  React.ReactNode;
  className?: string;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 px-2 py-0.5 rounded-full",
        "text-[10px] font-semibold leading-none tracking-wide",
        STYLES[variant],
        className
      )}
    >
      {children}
    </span>
  );
}

export function CredBadge({ score }: { score: number }) {
  const tier  = credibilityTier(score);
  const label = credibilityLabel(score);
  if (tier === "verified")   return <Badge variant="verified">✓ {label}</Badge>;
  if (tier === "trusted")    return <Badge variant="trusted">~ {label}</Badge>;
  return <Badge variant="unverified">! {label}</Badge>;
}

export function FactBadge({ status }: { status: FactCheckStatus }) {
  if (status === "clear")   return <Badge variant="verified">✓ No flags found</Badge>;
  if (status === "flagged") return <Badge variant="unverified">⚠ Claims flagged</Badge>;
  return <Badge variant="neutral">— Not checked</Badge>;
}