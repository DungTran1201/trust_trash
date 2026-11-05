export type SearchStatus = "completed" | "partial" | "failed";

export interface SearchRequest {
  query: string;
  source_ids?: string[];
  resource_types?: string[];
  limit_per_source?: number;
}

export interface SearchCoverage {
  source_id: string;
  status: "searched" | "partial" | "failed" | "skipped";
  reason?: string;
  result_count: number;
}
