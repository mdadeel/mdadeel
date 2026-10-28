# Arbor

**Architecture and health intelligence for GitHub repositories.** Connect a repository and get an inspectable map of its modules, its dependency graph, and a prioritised health report — so you understand the system before you change it.

<!-- Badges: uncomment the CI badge once the workflow has run green at least once.
[![CI](https://github.com/mdadeel/Arbor/actions/workflows/ci.yml/badge.svg)](https://github.com/mdadeel/Arbor/actions/workflows/ci.yml)
-->
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](./LICENSE)
[![Next.js](https://img.shields.io/badge/Next.js-15-000000?logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![tRPC](https://img.shields.io/badge/tRPC-11-2596BE)](https://trpc.io/)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)

<!-- SCREENSHOT: replace this block with 2–3 images, e.g.
<p align="center"><img src="docs/screenshots/architecture-map.png" alt="Interactive architecture map" width="85%"></p>
Save files under docs/screenshots/. See packaging/README.md in the planning repo.
-->

---

## Why

Every developer has opened an unfamiliar repository and had no idea where anything lived. Linters tell you about a line; they don't tell you how the system is shaped. Arbor answers the questions you ask in the first hour of a new codebase:

- What are the modules, and which ones actually depend on each other?
- Which files are load-bearing, and which are ignored but costly?
- Where is the risk — coupling, dead imports, leaked secrets, unowned code?
- What should I fix first, and what is the evidence?

Arbor produces a deterministic static analysis of the repository and renders it as an interactive graph plus a findings list. No workflow file, no local setup, no configuration.

## What it does

| Capability | Detail |
|---|---|
| **Architecture map** | Module graph from real import resolution (Babel AST), auto-laid out with dagre, interactive via React Flow. Cycle detection included. |
| **Health scoring** | Findings with file/line evidence, severity, confidence and recommended action — not a single opaque number. |
| **Dependency graph** | Normalised inventory of declared dependencies, plus SBOM generation (CycloneDX). |
| **Environment inventory** | Env-var discovery across `.env*` and config, with category and status tracking. |
| **API surface** | Detects OpenAPI/Swagger specs in the repo and parses them. |
| **Documentation hub** | Versioned documents with markdown editing and history. |
| **Commit and contributor timelines** | History through `simple-git`: recent commits, contributors, per-area ownership. |
| **PR checks** | GitHub webhook → queued analysis → Check Run with annotations on the pull request. |
| **Policy packs** | Versioned security / accessibility / maintainability policies, with workspace and project overrides and immutable snapshots. |
| **Triage** | Per-finding status, assignment and history, with stable fingerprints so triage survives re-scans. |
| **Trends & schedules** | Comparable scans over time, scheduled re-scans, notification preferences. |
| **Shareable reports** | Expiring, revocable share links that expose a limited, read-only projection. |
| **Patch suggestions** | Optional, review-only unified diffs from an LLM provider (BYOK). Never writes to a repository. |
| **Multi-tenant** | Workspaces, members, roles, invitations, audit log, admin console. |

Strict TypeScript throughout, 28 Prisma models, tRPC end to end.

## How analysis works

Arbor's default analysis is **deterministic**: it clones and reads the repository, parses imports with the Babel parser, resolves them against real paths and aliases, builds the graph, and runs rule-based checks. The same commit produces the same report.

An AI provider is **optional and opt-in** (OpenAI, Anthropic, or an OpenAI-compatible endpoint, key supplied by the user). It is used only for review-only patch suggestions. It never runs as part of the default audit, and no repository contents are sent anywhere unless a user explicitly configures a provider and requests a suggestion.

## Quick start

**Prerequisites:** Node.js 20+, Docker (for Postgres and Redis), a GitHub OAuth app.

```bash
git clone https://github.com/mdadeel/Arbor.git
cd Arbor

# 1. Start PostgreSQL and Redis
docker compose up -d

# 2. Install dependencies (runs `prisma generate`)
npm install

# 3. Configure environment
cp .env.example .env      # then fill in the values below

# 4. Apply migrations
npm run db:migrate

# 5. Run the app and the analysis worker
npm run dev:all           # web + worker
# or, in two terminals:
npm run dev               # Next.js on http://localhost:3000
npm run worker            # BullMQ worker
```

### Environment

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis connection string (BullMQ queues) |
| `NEXTAUTH_SECRET` | Session encryption secret (`openssl rand -base64 32`) |
| `NEXTAUTH_URL` | Canonical app URL |
| `GITHUB_ID` / `GITHUB_SECRET` | GitHub OAuth app credentials |
| `GITHUB_WEBHOOK_SECRET` | Verifies inbound webhook signatures |
| `GITHUB_APP_ID` / `GITHUB_APP_PRIVATE_KEY` | GitHub App for PR Check Runs (optional) |
| `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` | Only if you enable AI patch suggestions (or per-user BYOK) |

## Scripts

| Command | Does |
|---|---|
| `npm run dev` | Next.js dev server |
| `npm run dev:all` | Web server + analysis worker |
| `npm run worker` | BullMQ worker only |
| `npm run build` | `prisma generate` + production build |
| `npm run typecheck` | `tsc --noEmit` |
| `npm run lint` | ESLint |
| `npm test` | Vitest (unit + component) |
| `npm run test:e2e` | Playwright |
| `npm run db:migrate` | `prisma migrate dev` |
| `npm run analyze:local -- <dir>` | Run the analyser against a local directory, no DB needed |

## Architecture

```
src/
├── app/                 Next.js App Router
│   ├── (auth)/          sign-in, admin sign-in
│   ├── (dashboard)/     projects, systems, settings
│   ├── admin/           users, roles, workspaces, audit, waitlist, email
│   ├── api/             tRPC handler, GitHub webhook, worker, badges, shares
│   └── share/[token]/   public read-only report
├── components/
│   ├── dashboard/       architecture canvas, findings, docs, commits, triage
│   └── marketing/       landing page sections
├── server/
│   ├── routers/         tRPC routers
│   └── services/        analysis, auth/access, policy, triage, AI, SBOM
└── worker/              BullMQ processors
prisma/                  schema.prisma + 9 migrations
```

- **Web:** Next.js 15 (App Router), React 18, Tailwind, Radix, Recharts, React Flow.
- **API:** tRPC 11 (superjson), Zod validation, NextAuth v4 with GitHub OAuth.
- **Async:** BullMQ on Redis; analyses are queued and processed by a separate worker with atomic state transitions and stale-run cleanup.
- **Data:** PostgreSQL + Prisma.
- **Access control:** workspace membership and role checks enforced in services, not only in routers — including revalidation after membership changes.

## Status

Arbor is an **actively developed product preview**, not a finished commercial release. Being specific:

- ✅ Unit and component tests pass locally (52 test files, 259 tests). Lint passes.
- ⚠️ The GitHub webhook + Check Run path is implemented and unit-tested but has **not** been verified against a live GitHub App installation.
- ⚠️ `npm run typecheck` currently reports diagnostics in environments where the Prisma client is not generated from the real schema; a clean `typecheck` + `build` against a generated client is the immediate priority.
- ⚠️ Integration tests against real PostgreSQL and Redis are not yet wired into CI.
- ⛔ **No billing is implemented.** The pricing page shows a Teams tier as a waitlist; nothing charges anyone.
- ⛔ Self-hosting is supported via `docker compose` for Postgres/Redis, but there is no single-image deployment yet.

The detailed, phase-by-phase state of this work lives in [`docs/backend-review-feature-roadmap.md`](./docs/backend-review-feature-roadmap.md). It is deliberately honest about what is verified and what isn't.

## Roadmap

- [ ] Green CI: typecheck → lint → test → build on every PR
- [ ] SARIF export, so findings appear in GitHub Code Scanning
- [ ] Hotspot analysis (churn × complexity per file)
- [ ] Suggested `CODEOWNERS` and bus-factor per directory
- [ ] Scan-to-scan diff view ("what changed since last week")
- [ ] Single-image self-hosted deployment
- [ ] Official CycloneDX schema validation
- [ ] Monorepo/workspace-aware graphs (pnpm, turborepo, Nx)

## Contributing

Issues and pull requests are welcome. Please run `npm run lint`, `npm run typecheck` and `npm test` before opening a PR. For anything larger than a bug fix, open an issue first so the design can be discussed.

## Licence

**AGPL-3.0.** You can self-host Arbor, modify it, and use it internally for free. If you offer a modified version as a network service, the AGPL requires you to publish your changes under the same licence.

For use that the AGPL doesn't suit — hosting Arbor for clients without publishing modifications, embedding it in a commercial product, or white-label deployment — a **commercial licence** is available: [shahnawasadeel@gmail.com](mailto:shahnawasadeel@gmail.com).

See [`LICENSE`](./LICENSE).

---

Built by [Shahnawas Adeel](https://mdadeel.me) · [LinkedIn](https://www.linkedin.com/in/shahnawasadee1/)
