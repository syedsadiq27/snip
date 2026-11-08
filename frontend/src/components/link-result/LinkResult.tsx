import { useState } from 'react';

import type { LinkResponse } from '../../api/types';

type LinkResultProps = {
  link: LinkResponse;
};

export function LinkResult({ link }: LinkResultProps) {
  const [copied, setCopied] = useState(false);

  async function copyShortUrl() {
    try {
      await navigator.clipboard.writeText(link.short_url);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setCopied(false);
    }
  }

  return (
    <section
      aria-live="polite"
      className="animate-rise grid gap-4 rounded-2xl border border-[var(--line)] bg-white/90 p-5 shadow-md sm:p-6"
    >
      <div className="grid gap-1">
        <p className="font-display text-xl text-[var(--ink)] sm:text-2xl">
          Your short link is ready
        </p>
        <p className="truncate text-sm text-[var(--ink-muted)]">
          {link.original_url}
        </p>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <a
          href={link.short_url}
          target="_blank"
          rel="noreferrer"
          className="min-w-0 flex-1 break-all font-mono text-lg text-[var(--accent-deep)] underline-offset-4 hover:underline"
        >
          {link.short_url}
        </a>
        <button
          type="button"
          onClick={copyShortUrl}
          className="shrink-0 rounded-xl bg-[var(--ink)] px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-[var(--ink-soft)]"
        >
          {copied ? 'Copied' : 'Copy'}
        </button>
      </div>

      <dl className="grid gap-3 text-sm text-[var(--ink-muted)] sm:grid-cols-3">
        <div className="grid gap-1">
          <dt className="uppercase tracking-wide">Alias</dt>
          <dd className="font-medium text-[var(--ink)]">{link.alias}</dd>
        </div>
        <div className="grid gap-1">
          <dt className="uppercase tracking-wide">Visits</dt>
          <dd className="font-medium text-[var(--ink)]">{link.visit_count}</dd>
        </div>
        <div className="grid gap-1">
          <dt className="uppercase tracking-wide">Expires</dt>
          <dd className="font-medium text-[var(--ink)]">
            {link.expires_at
              ? new Date(link.expires_at).toLocaleString()
              : 'Never'}
          </dd>
        </div>
      </dl>
    </section>
  );
}
