# AGENTS.md

## Repository state

- Bare repo: `README.md` is a single-line title; no source, no manifests, no build/test/lint config, no CI, no instruction files.
- Single commit `5f5682b "Initial commit"`, branch `main`, working tree clean.

## Guidance

- Do not assume a language, framework, or toolchain exists here — none is configured yet.
- Before writing guidance into this file, verify it against real source/config; anything here should only document facts that are actually present.
- No developer commands exist to run yet. If work adds code or config, update this file with the exact commands and structure that emerge.

## Python script (`main.py`)

- `main.py` fetches public Google Play reviews for the Roblox Android app (`com.roblox.client`) via `google_play_scraper.reviews()` and returns a pandas DataFrame (columns: `reviews_text`, `rating`, `timestamp`).
- `reviews()` returns a plain `(reviews_list, continuation_token)` tuple in google-play-scraper 1.2.7 — not a generator, so do not call `next()` on it.
- `analyze_sentiment()` adds VADER columns `pos`, `neu`, `neg`, `compound` and a `sentiment_label` (`positive`/`neutral`/`negative` via compound ± 0.05).
- Dependencies: `pandas`, `google-play-scraper`, `vaderSentiment` (no manifest — install with `pip install pandas google-play-scraper vaderSentiment`).
- Run: `python main.py` (uses the system Python 3.14). On Windows the script reconfigures stdout to UTF-8 because the default cp1252 console crashes on non-ASCII review text.
- VADER is English-only; the fetch therefore uses `lang='en'` so sentiment scores are meaningful.