export type CategorySlug =
  | "ai"
  | "technology"
  | "education"
  | "politics"
  | "business"
  | "startups"
  | "world"
  | "sports"
  | "health";

export type FactCheckStatus = "clear" | "flagged" | "unchecked";

export type FreshnessWindow = 6 | 24 | 48;

export type ToastType = "success" | "error" | "info" | "warning";

export interface ToastItem {
  id:      string;
  message: string;
  type:    ToastType;
}

export interface Article {
  id:                       string;
  title:                    string;
  summary:                  string | null;
  category:                 CategorySlug;
  source_name:              string;
  source_url:               string | null;
  canonical_url:            string | null;
  image_url:                string | null;
  author:                   string | null;
  published_at:             string;
  credibility_score:        number;
  freshness_score:          number;
  composite_score:          number | null;
  fact_check_status:        FactCheckStatus;
  is_breaking:              boolean;
  is_cluster_representative: boolean;
  duplicate_cluster_id:     string | null;
  cluster_source_count:     number;
  tags:                     string[];
}

export interface Source {
  id:                string;
  name:              string;
  slug:              string;
  domain:            string;
  credibility_score: number;
  bias_label:        string | null;
  category:          string | null;
  country:           string;
  article_count:     number;
}

export interface CategoryInfo {
  slug:          CategorySlug;
  label:         string;
  article_count: number;
  latest_at:     string | null;
}

export interface PaginatedResponse<T> {
  total:     number;
  page:      number;
  page_size: number;
  results:   T[];
}