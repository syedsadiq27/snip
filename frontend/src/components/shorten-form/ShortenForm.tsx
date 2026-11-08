import { useState, type FormEvent } from 'react';

export type ShortenFormValues = {
  url: string;
  alias: string;
  expiresAt: string;
};

type ShortenFormProps = {
  busy: boolean;
  error: string | null;
  onSubmit: (values: ShortenFormValues) => void;
};

export function ShortenForm({ busy, error, onSubmit }: ShortenFormProps) {
  const [url, setUrl] = useState('');
  const [alias, setAlias] = useState('');
  const [expiresAt, setExpiresAt] = useState('');
  const [showOptions, setShowOptions] = useState(false);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSubmit({ url: url.trim(), alias: alias.trim(), expiresAt });
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="grid w-full gap-4 rounded-2xl bg-white/80 p-5 shadow-md backdrop-blur-sm sm:p-6"
    >
      <label className="grid gap-2">
        <span className="text-sm font-medium text-[var(--ink-muted)]">
          Long URL
        </span>
        <input
          required
          type="url"
          name="url"
          value={url}
          onChange={(event) => setUrl(event.target.value)}
          placeholder="https://example.com/very/long/path"
          className="w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-4 py-3 text-base text-[var(--ink)] outline-none transition focus:border-[var(--accent)] focus:ring-2 focus:ring-[var(--accent-soft)]"
        />
      </label>

      <button
        type="button"
        onClick={() => setShowOptions((open) => !open)}
        className="justify-self-start text-sm font-medium text-[var(--accent-deep)] underline-offset-4 transition hover:underline"
      >
        {showOptions ? 'Hide options' : 'Custom alias & expiry'}
      </button>

      {showOptions ? (
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="grid gap-2">
            <span className="text-sm font-medium text-[var(--ink-muted)]">
              Custom alias
            </span>
            <input
              type="text"
              name="alias"
              value={alias}
              onChange={(event) => setAlias(event.target.value)}
              placeholder="my-link"
              minLength={3}
              maxLength={32}
              pattern="[A-Za-z0-9_-]+"
              title="Letters, digits, underscores, hyphens (3–32)"
              className="w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-4 py-3 text-base text-[var(--ink)] outline-none transition focus:border-[var(--accent)] focus:ring-2 focus:ring-[var(--accent-soft)]"
            />
          </label>
          <label className="grid gap-2">
            <span className="text-sm font-medium text-[var(--ink-muted)]">
              Expires at
            </span>
            <input
              type="datetime-local"
              name="expiresAt"
              value={expiresAt}
              onChange={(event) => setExpiresAt(event.target.value)}
              className="w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-4 py-3 text-base text-[var(--ink)] outline-none transition focus:border-[var(--accent)] focus:ring-2 focus:ring-[var(--accent-soft)]"
            />
          </label>
        </div>
      ) : null}

      {error ? (
        <p
          role="alert"
          className="rounded-xl bg-[var(--danger-soft)] px-4 py-3 text-sm text-[var(--danger)]"
        >
          {error}
        </p>
      ) : null}

      <button
        type="submit"
        disabled={busy || !url.trim()}
        className="inline-flex items-center justify-center rounded-xl bg-[var(--accent)] px-5 py-3 text-base font-semibold text-[var(--accent-ink)] shadow-md transition hover:-translate-y-0.5 hover:bg-[var(--accent-deep)] disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:translate-y-0"
      >
        {busy ? 'Shortening…' : 'Shorten link'}
      </button>
    </form>
  );
}
