import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { formatDistanceToNow, parseISO } from "date-fns";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function timeAgo(dateString: string): string {
  try {
    return formatDistanceToNow(parseISO(dateString), { addSuffix: true });
  } catch {
    return "recently";
  }
}

export function formatScore(score: number): string {
  return `${Math.round(score * 100)}%`;
}

export function credibilityTier(score: number): "verified" | "trusted" | "unverified" {
  if (score >= 0.88) return "verified";
  if (score >= 0.70) return "trusted";
  return "unverified";
}

export function credibilityLabel(score: number): string {
  const tier = credibilityTier(score);
  if (tier === "verified")   return "Verified";
  if (tier === "trusted")    return "Trusted";
  return "Unverified";
}

export function truncate(str: string, max: number): string {
  if (str.length <= max) return str;
  return str.slice(0, max).trimEnd() + "…";
}