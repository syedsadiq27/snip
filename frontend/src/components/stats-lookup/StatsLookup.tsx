import { useState, type FormEvent } from 'react';

import { getLinkStats } from '../../api/client';
import type { LinkStatsResponse } from '../../api/types';

export function StatsLookup() {
  const [alias, setAlias] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState<LinkStatsResponse | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const cleaned = alias.trim();
    if (!cleaned) {
      return;
    }

    setBusy(true);
    setError(null);
    setStats(null);

    try {
      const result = await getLinkStats(cleaned);
      setStats(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load stats');
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="grid gap-6">
      <div className="grid max-w-xl gap-2">
        <h2 className="font-display text-3xl text-[var(--ink)] sm:text-4xl">
          Check a link
        </h2>
        <p className="text-base text-[var(--ink-muted)]">
          Look up visits, expiry, and destination for any alias.
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="grid gap-4 rounded-2xl bg-white/80 p-5 shadow-md backdrop-blur-sm sm:grid-cols-[1fr_auto] sm:items-end sm:p-6"
      >
        <label className="grid gap-2">
          <span className="text-sm font-medium text-[var(--ink-muted)]">
            Alias
          </span>
          <input
            required
            type="text"
            value={alias}
            onChange={(event) => setAlias(event.target.value)}
            placeholder="my-link"
            className="w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-4 py-3 text-base text-[var(--ink)] outline-none transition focus:border-[var(--accent)] focus:ring-2 focus:ring-[var(--accent-soft)]"
          />
        </label>
        <button
          type="submit"
          disabled={busy || !alias.trim()}
          className="rounded-xl bg-[var(--ink)] px-5 py-3 text-base font-semibold text-white transition hover:bg-[var(--ink-soft)] disabled:cursor-not-allowed disabled:opacity-60"
        >
          {busy ? 'Loading…' : 'Get stats'}
        </button>
      </form>

      {error ? (
        <p
          role="alert"
          className="rounded-xl bg-[var(--danger-soft)] px-4 py-3 text-sm text-[var(--danger)]"
        >
          {error}
        </p>
      ) : null}

      {stats ? (
        <dl className="animate-rise grid gap-4 rounded-2xl border border-[var(--line)] bg-white/90 p-5 shadow-md sm:grid-cols-2 sm:p-6">
          <div className="grid gap-1 sm:col-span-2">
            <dt className="text-sm uppercase tracking-wide text-[var(--ink-muted)]">
              Short URL
            </dt>
            <dd>
              <a
                href={stats.short_url}
                target="_blank"
                rel="noreferrer"
                className="break-all font-mono text-[var(--accent-deep)] underline-offset-4 hover:underline"
              >
                {stats.short_url}
              </a>
            </dd>
          </div>
          <div className="grid gap-1 sm:col-span-2">
            <dt className="text-sm uppercase tracking-wide text-[var(--ink-muted)]">
              Destination
            </dt>
            <dd className="break-all text-[var(--ink)]">
              {stats.original_url}
            </dd>
          </div>
          <div className="grid gap-1">
            <dt className="text-sm uppercase tracking-wide text-[var(--ink-muted)]">
              Visits
            </dt>
            <dd className="text-2xl font-semibold text-[var(--ink)]">
              {stats.visit_count}
            </dd>
          </div>
          <div className="grid gap-1">
            <dt className="text-sm uppercase tracking-wide text-[var(--ink-muted)]">
              Status
            </dt>
            <dd
              className={`text-2xl font-semibold ${
                stats.expired ? 'text-[var(--danger)]' : 'text-[var(--ok)]'
              }`}
            >
              {stats.expired ? 'Expired' : 'Active'}
            </dd>
          </div>
          <div className="grid gap-1">
            <dt className="text-sm uppercase tracking-wide text-[var(--ink-muted)]">
              Created
            </dt>
            <dd className="text-[var(--ink)]">
              {new Date(stats.created_at).toLocaleString()}
            </dd>
          </div>
          <div className="grid gap-1">
            <dt className="text-sm uppercase tracking-wide text-[var(--ink-muted)]">
              Expires
            </dt>
            <dd className="text-[var(--ink)]">
              {stats.expires_at
                ? new Date(stats.expires_at).toLocaleString()
                : 'Never'}
            </dd>
          </div>
        </dl>
      ) : null}
    </section>
  );
}
