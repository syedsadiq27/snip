export type CreateLinkPayload = {
  url: string;
  alias?: string | null;
  expires_at?: string | null;
};

export type LinkResponse = {
  alias: string;
  short_url: string;
  original_url: string;
  created_at: string;
  expires_at: string | null;
  visit_count: number;
};

export type LinkStatsResponse = LinkResponse & {
  expired: boolean;
};

export type ApiError = {
  detail: string;
};
