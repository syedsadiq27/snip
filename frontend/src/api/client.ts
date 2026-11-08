import type {
  ApiError,
  CreateLinkPayload,
  LinkResponse,
  LinkStatsResponse,
} from './types';

const API_BASE =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? '';

async function parseError(response: Response): Promise<never> {
  let detail = `Request failed (${response.status})`;
  try {
    const body = (await response.json()) as ApiError;
    if (typeof body.detail === 'string' && body.detail.trim()) {
      detail = body.detail;
    }
  } catch {
    void 0;
  }
  throw new Error(detail);
}

export async function createLink(
  payload: CreateLinkPayload
): Promise<LinkResponse> {
  const response = await fetch(`${API_BASE}/api/links`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      url: payload.url,
      alias: payload.alias || null,
      expires_at: payload.expires_at || null,
    }),
  });

  if (!response.ok) {
    await parseError(response);
  }

  return (await response.json()) as LinkResponse;
}

export async function getLinkStats(alias: string): Promise<LinkStatsResponse> {
  const response = await fetch(
    `${API_BASE}/api/links/${encodeURIComponent(alias)}`
  );

  if (!response.ok) {
    await parseError(response);
  }

  return (await response.json()) as LinkStatsResponse;
}
