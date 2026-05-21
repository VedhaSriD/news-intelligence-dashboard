import type {
  Article,
  CategoryInfo,
  PaginatedResponse,
  Source,
  CategorySlug,
} from "@/types";
import { MOCK_ARTICLES } from "@/lib/constants";

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function apiFetch<T>(
  path: string,
  params?: Record<string, string | number | undefined>
): Promise<T> {
  const url = new URL(`${BASE}${path}`);
  if (params) {
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined) url.searchParams.set(k, String(v));
    });
  }
  const res = await fetch(url.toString(), {
    headers: { "Content-Type": "application/json" },
    next: { revalidate: 60 },
  });
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
}

export const articlesApi = {
  latest: (p?: { hours?: number; category?: CategorySlug; page?: number; page_size?: number }) =>
    apiFetch<PaginatedResponse<Article>>("/api/v1/articles/latest", p),

  archive: (p: { date: string; category?: CategorySlug; page?: number }) =>
    apiFetch<PaginatedResponse<Article>>("/api/v1/articles/archive", p),

  search: (q: string, category?: CategorySlug) =>
    apiFetch<PaginatedResponse<Article>>("/api/v1/articles/search", { q, ...(category ? { category } : {}) }),
};

export const categoriesApi = {
  list: () => apiFetch<CategoryInfo[]>("/api/v1/categories"),
};

export const sourcesApi = {
  list: () => apiFetch<Source[]>("/api/v1/sources"),
};

// Falls back to MOCK_ARTICLES if backend is offline
export async function fetchLatestWithFallback(
  hours: number,
  category?: CategorySlug | null
): Promise<{ articles: Article[]; isDemo: boolean }> {
  try {
    const data = await articlesApi.latest({ hours, category: category ?? undefined, page_size: 30 });
    return { articles: data.results, isDemo: false };
  } catch {
    const all = MOCK_ARTICLES as Article[];
    return {
      articles: category ? all.filter((a) => a.category === category) : all,
      isDemo: true,
    };
  }
}