import { useState } from 'react';

import { createLink } from './api/client';
import type { LinkResponse } from './api/types';
import { LinkResult } from './components/link-result';
import { ShortenForm, type ShortenFormValues } from './components/shorten-form';
import { StatsLookup } from './components/stats-lookup';

function toExpiresAtIso(localValue: string): string | null {
  if (!localValue) {
    return null;
  }
  const date = new Date(localValue);
  if (Number.isNaN(date.getTime())) {
    throw new Error('Invalid expiry date');
  }
  return date.toISOString();
}

export default function App() {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [created, setCreated] = useState<LinkResponse | null>(null);

  async function handleShorten(values: ShortenFormValues) {
    setBusy(true);
    setError(null);

    try {
      const expiresAt = toExpiresAtIso(values.expiresAt);
      const link = await createLink({
        url: values.url,
        alias: values.alias || null,
        expires_at: expiresAt,
      });
      setCreated(link);
    } catch (err) {
      setCreated(null);
      setError(err instanceof Error ? err.message : 'Failed to create link');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="relative min-h-screen overflow-x-hidden">
      <div className="pointer-events-none absolute inset-0 -z-10 bg-mesh" />
      <div className="pointer-events-none absolute inset-x-0 top-0 -z-10 h-[85vh]">
        <div className="bg-hero-band absolute inset-0" />
        <div className="hero-plane" />
      </div>

      <header className="mx-auto flex w-full max-w-5xl items-center justify-between px-6 pt-8">
        <p className="font-display text-3xl tracking-tight text-[var(--ink)] sm:text-4xl">
          Snip
        </p>
        <a
          href="#stats"
          className="text-sm font-medium text-[var(--ink-muted)] transition hover:text-[var(--ink)]"
        >
          Link stats
        </a>
      </header>

      <main>
        <section className="mx-auto grid min-h-[calc(100vh-5rem)] w-full max-w-5xl content-center gap-10 px-6 py-16 lg:grid-cols-[1.05fr_0.95fr] lg:items-center lg:gap-14 lg:py-10">
          <div className="animate-fade-up grid gap-5">
            <p className="font-display text-6xl leading-none tracking-tight text-[var(--ink)] sm:text-7xl lg:text-8xl">
              Snip
            </p>
            <h1 className="max-w-md text-xl leading-snug text-[var(--ink-soft)] sm:text-2xl">
              Turn long URLs into links people will actually share.
            </h1>
            <p className="max-w-sm text-base text-[var(--ink-muted)]">
              Custom aliases, optional expiry, and visit stats — no account
              required.
            </p>
          </div>

          <div className="animate-fade-up-delayed grid gap-5">
            <ShortenForm busy={busy} error={error} onSubmit={handleShorten} />
            {created ? <LinkResult link={created} /> : null}
          </div>
        </section>

        <section
          id="stats"
          className="border-t border-[var(--line)] bg-[var(--surface-alt)]/70"
        >
          <div className="mx-auto w-full max-w-5xl px-6 py-20">
            <StatsLookup />
          </div>
        </section>
      </main>

      <footer className="mx-auto w-full max-w-5xl px-6 py-8 text-sm text-[var(--ink-muted)]">
        Snip · FastAPI + React
      </footer>
    </div>
  );
}
