# PinFlow

**Turn a folder of product images into a scheduled, searchable Pinterest presence.** Drop images in, get AI-generated titles, descriptions and alt text, mapped to the right board, queued on a posting schedule, and tracked for performance.

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15-000000?logo=nextdotjs&logoColor=white)](https://nextjs.org/)

---

## The problem

Small commerce sellers know Pinterest drives traffic, and still don't post, because the work is tedious: write a caption, pick keywords, choose a board, find the right moment, repeat for every image. PinFlow automates the repetitive part and leaves the judgement to you.

## What it does

| Stage | Detail |
|---|---|
| **Ingest** | Watch a folder for new images, or upload through the web UI; bulk CSV import for batches |
| **Understand** | A vision model reads each image and produces a title, description, alt text, tags and a suggested board/category — batched, with rate-limit protection |
| **Route** | Category → board mapping, with explicit overrides when the AI guess is wrong |
| **Schedule** | Posting slots per day (`POST_HOURS`, `POSTS_PER_DAY`), a queue with retry, and a calendar view |
| **Publish** | Sends to Pinterest through the official API using a user access token |
| **Measure** | Per-pin analytics, queue history and performance reporting |

The web app has: dashboard, upload, queue, calendar, pin detail, analytics, and privacy pages — built on Next.js with a component test suite.

## Architecture

```
pinterest_automation/          Python backend
├── api/                       HTTP layer (FastAPI)
├── services/
│   ├── analyzer.py            vision analysis + batching
│   ├── board_mapper.py        category → board resolution
│   ├── scheduler.py           slot allocation, queue, retry
│   ├── pin_actions.py         publish / update / delete
│   ├── analytics_service.py   performance rollups
│   ├── seo_generator.py       keyword-oriented copy
│   └── gemini_sidecar.py      local OpenAI-compatible vision proxy
├── processors/                image + batch workers
├── storage/                   database + file storage
└── config/settings.py         typed settings

pinterest-web/                 Next.js front end (App Router)
```

**Providers are pluggable.** Any OpenAI-compatible endpoint works — OpenRouter with a hosted vision model, or the bundled local Gemini Web2API sidecar, or another provider with an OpenAI-shaped API. Configure via `LLM_PROVIDERS`.

## Quick start

```bash
git clone https://github.com/mdadeel/pinflow.git
cd pinflow

python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

cp .env.example .env            # fill in the values below

# backend
./venv/bin/python -m pinterest_automation.main serve

# frontend (second terminal)
cd pinterest-web
npm install
npm run dev                     # http://localhost:3000
```

### Configuration

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `OPENROUTER_API_KEY` | yes* | — | Vision metadata generation |
| `PINTEREST_ACCESS_TOKEN` | yes | — | Publishing (scopes: `boards:read`, `pins:read`, `pins:write`, `user_accounts:read`) |
| `PINTEREST_BOARD_ID` | no | — | Fallback board when category mapping misses |
| `OPENROUTER_MODEL` | no | `google/gemini-2.5-flash` | Vision model |
| `LLM_PROVIDERS` | no | — | JSON array of providers; use this to run against a local sidecar instead |
| `ANALYSIS_WORKERS` | no | `2` | Concurrent model calls |
| `AI_CALL_DELAY_SECONDS` | no | `1.0` | Delay between calls (rate-limit protection) |
| `POSTS_PER_DAY` | no | `50` | Daily publish cap |
| `POST_HOURS` | no | `8,11,14,17,20` | Posting slots (UTC) |
| `BATCH_SIZE` | no | `25` | Images per analysis batch |
| `WATCH_DIR` | no | `./images` | Folder watched for new images |
| `BOARD_OVERRIDES` | no | `{}` | JSON map of category → board ID |

\* not required if you run entirely against a local `LLM_PROVIDERS` endpoint.

Rate limits are real: a hosted vision provider will return `HTTP 429` if you push too hard. Lower `ANALYSIS_WORKERS` and raise `AI_CALL_DELAY_SECONDS` before assuming a bug.

## Using it responsibly

- Publishing must go through the **official Pinterest API** with a token you own. Scraping, or automating a browser session, violates Pinterest's terms and risks an account ban — don't do it, and don't ship a feature that does.
- Every generated caption is a **draft**. Review before publishing; the model will occasionally mislabel an image or over-optimise keywords.
- Respect Pinterest's rate limits and your own posting cadence. Flooding a board is a spam signal.

If you need multi-account or team features, the compliant path is an approved Pinterest app plus per-user OAuth — not token sharing.

## Status

- ✅ End-to-end flow works: ingest → analyse → route → schedule → publish → report.
- ✅ Batching, retry and rate-limit handling are implemented in the scheduler and processor layers.
- ✅ Front end covers dashboard, upload, queue, calendar, pin detail and analytics, with component tests.
- ⚠️ Single-user by design: one token, one account. Multi-tenant OAuth is not implemented.
- ⚠️ `ENTERPRISE_PLAN.md` is a self-assessment with an open list (API authentication enforcement first among them). Read it before deploying for anyone but yourself.
- ⚠️ No CI yet.

## Roadmap

- [ ] Enforce API authentication on every endpoint (currently the top item in `ENTERPRISE_PLAN.md`)
- [ ] Per-user OAuth so multiple accounts can be managed safely
- [ ] CI: ruff + pytest on the backend, build + test on the web app
- [ ] Content repurposing beyond Pinterest: one product image → caption set for Instagram, Facebook and story formats
- [ ] Draft review queue with approve/reject before anything publishes
- [ ] Cost and rate telemetry per provider

## Licence

**AGPL-3.0.** Self-host and modify freely; if you run a modified version as a network service, publish your changes. A commercial licence is available for hosted or white-label use: [shahnawasadeel@gmail.com](mailto:shahnawasadeel@gmail.com). See [`LICENSE`](./LICENSE).

---

Built by [Shahnawas Adeel](https://mdadeel.me)
