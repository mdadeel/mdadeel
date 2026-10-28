# Arbor — handover prompt for the next session

**Purpose:** a copy-paste brief so a fresh session connected to `mdadeel/Arbor` can do the work without rediscovering the codebase.
**Nothing in this file changes Arbor.** It is a specification, not a patch.

---

## How to use it

1. Open a new session and connect **only** the `mdadeel/Arbor` repository.
2. Paste **§1 (the master prompt)** as your first message.
3. Let it finish Phase 0 and Phase 1, then review the PR.
4. For later phases, paste the prompt in §3 for that phase.

Do not paste all phases at once — a single session that tries to do everything will produce a large, unreviewable PR and will probably leave the build broken.

---

## §0 — Verified facts about the repo (the prompt relies on these)

Read from the code on `main`, 28 Oct 2026. The other session should re-verify, not trust blindly.

| Item | Reality |
|---|---|
| Framework | Next.js `^15.5.27` (README wrongly says 14), React 18, TS 5.9 strict, tRPC `^11.0.0-rc.364` (**release candidate**), Prisma 5.10 |
| Size | ~41k LOC TS/TSX, 265 files in `src/`, 28 Prisma models, 9 migrations |
| Env schema | **`src/lib/env.ts`** (t3-env + Zod) is the single source of truth — see §2 for the real variable names |
| `.env.example` | **Does not exist.** The README's quick start cannot work as written |
| CI | **No `.github/` directory at all** |
| Licence | None |
| Worker | Two paths: BullMQ (`src/worker/`) and a serverless fallback at `src/app/api/worker/process/route.ts`, guarded by `CRON_SECRET`, triggered by `vercel.json` cron **once a day at 03:00 UTC**, `maxDuration = 300` |
| Billing | **No billing code exists.** `pricing-section.tsx` advertises a `$15/month` Teams tier as a waitlist only |
| PDF export | **None.** `ProjectReport` (`src/components/dashboard/project-report.tsx`) and the share page render HTML only; no `@media print`, no exporter |
| Share links | Fully implemented incl. hashed tokens, expiry and revocation (`src/server/services/report-sharing.ts`) |
| Tests | 53 test files, Vitest + Testing Library; Playwright configured but not run in CI |
| Docs | `README.md` links `.ai/architecture.md` and `docs/architecture/` — **neither exists**. Only `docs/backend-review-feature-roadmap.md` is real |
| Docker | `docker-compose.yml` covers **Postgres + Redis only**; no `Dockerfile` for the app |

---

## §1 — The master prompt (copy all of this into the new session)

```text
You are working in the mdadeel/Arbor repository. Arbor is a developer tool that audits a
GitHub repository and produces an architecture map, a health report and prioritised findings.
It is a real product with paying-customer intent, currently in a "product preview" state.

Hard rules for this session:
- Work on a branch named chore/production-readiness and open ONE pull request at the end.
  Never commit directly to main. Never force-push main.
- Do not rewrite the analysis engine, the Prisma schema, or the tRPC API surface. This task is
  build integrity, CI, licensing and documentation accuracy — not new features.
- Every claim you put in a README or a status section must be verified by running a command.
  If you cannot verify it, write "unverified" instead of asserting it.
- Keep TypeScript strict. Do not add `any`, `@ts-ignore`, or `@ts-expect-error` to silence errors.
  Do not change tsconfig to weaken checks.
- Do not commit secrets. Generate placeholders in .env.example only.
- Run the full verification command after each step, not once at the end.

VERIFICATION COMMAND (this is the definition of done for this session):
  npm ci && npx prisma generate && npx prisma validate && npm run typecheck && npm run lint && npm test -- --run && npm run build

PHASE 0 — make the repo verifiable

Task 0.1  Read src/lib/env.ts first. It is the authoritative environment contract, and it is
          validated at import time with Zod. Then grep for process.env usages that bypass it:
              grep -rhoE "process\.env\.[A-Z_0-9]+" src scripts prisma | sort -u
          Create .env.example at the repo root containing EVERY variable, grouped with comments:
            - Required (no default): DATABASE_URL, REDIS_URL, NEXTAUTH_SECRET, ENCRYPTION_SECRET
            - Optional with defaults: CLONE_BASE_DIR, CLONE_TIMEOUT, MAX_REPO_SIZE_MB, MAX_FILES,
              MAX_FILE_SIZE_KB, MAX_PARSE_FILES, ANALYSIS_TIMEOUT_MS, APP_URL, CRON_SECRET,
              GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, GITHUB_WEBHOOK_SECRET, ADMIN_EMAILS,
              ADMIN_GITHUB_USERNAMES, ADMIN_USERNAME, ADMIN_PASSWORD
            - Also used at runtime but NOT in env.ts: RESEND_API_KEY, EMAIL_FROM, APP_TOKEN,
              SECRET_KEY, NEXT_PUBLIC_API_URL, NEXTAUTH_URL
          Use obviously-fake placeholder values, and add a comment above ENCRYPTION_SECRET
          explaining it encrypts stored user AI provider keys, so rotating it invalidates them.
          Add a comment that ADMIN_USERNAME/ADMIN_PASSWORD enable credential login and must stay
          empty in production.

Task 0.2  Run `npx prisma generate`, then `npm run typecheck` and capture the FULL list of
          diagnostics into docs/typecheck-baseline.md (file, line, code, message) before fixing
          anything. If the list is empty, record that instead. Do not skip this step: the repo
          roadmap claims 105 diagnostics, and we need to know the real number, not a guess.

Task 0.3  Fix the typecheck errors, in this order:
            1. Prisma inference problems (regenerate the client; never hand-write types)
            2. Genuine logic or null-safety bugs
            3. Narrowing issues that need a real type guard
          For each error you cannot fix without changing behaviour, stop and list it for review
          rather than casting it away. Report the before/after count in the PR description.

Task 0.4  `npm run lint` currently calls `next lint`, which is deprecated in Next 15. Migrate to
          the ESLint CLI: update the script and add a flat or eslintrc config consistent with the
          existing .eslintrc.json, whichever works with the installed ESLint 8 without changing
          which rules apply. `npm run lint` must pass with zero warnings before you finish.

Task 0.5  Add .github/workflows/ci.yml with two jobs on Node 20 and these service containers:
          postgres:16 (user/pass/db = arbor) and redis:7.
          Steps for job "verify": checkout, setup-node with npm cache, npm ci, npx prisma validate,
          npx prisma migrate deploy, npm run typecheck, npm run lint, npm test -- --run.
          Steps for job "build": npm ci, npm run build, needs: verify.
          Env for both jobs — use exactly these names, they must match src/lib/env.ts:
            DATABASE_URL: postgresql://arbor:arbor@localhost:5432/arbor
            REDIS_URL: redis://localhost:6379
            NEXTAUTH_SECRET and ENCRYPTION_SECRET: any non-empty CI placeholder
              (ENCRYPTION_SECRET is REQUIRED by the Zod schema — omitting it fails the build)
            CRON_SECRET: any non-empty CI placeholder
            APP_URL: http://localhost:3000
          Use `concurrency` to cancel superseded runs. Do NOT add continue-on-error to any step.

Task 0.6  Run the workflow on the PR. Iterate until BOTH jobs are green. Only then, uncomment
          the CI badge in README.md. If a job cannot be made green, leave the badge commented and
          say precisely which step fails and why. A badge that lies is worse than no badge.

Task 0.7  Add LICENSE at the repo root: GNU AGPL-3.0 (verbatim text, with
          "Copyright (C) 2026 Shahnawas Adeel" prepended). Then add a short "Licence" section to
          README.md saying: self-hosting and modification are free; offering a modified version as
          a network service requires publishing changes under the AGPL; a commercial licence is
          available for white-label or closed-source hosting, contact shahnawasadeel@gmail.com.

Task 0.8  Rewrite README.md to match reality. Requirements:
          - Fix "Next.js 14" to 15 in the tech stack.
          - Fix the environment section to use the REAL variable names from src/lib/env.ts
            (GITHUB_CLIENT_ID / GITHUB_CLIENT_SECRET, not GITHUB_ID / GITHUB_SECRET; and add
            ENCRYPTION_SECRET, CRON_SECRET, CLONE_*, ADMIN_*). Do not invent variables.
          - Add `cp .env.example .env` as a step in Quick Start.
          - Add "run the worker" to Quick Start (npm run worker, or npm run dev:all) and explain
            that analyses are queued and will not complete without a worker.
          - REMOVE the sentence pointing at .ai/architecture.md and docs/architecture/ — neither
            exists. Replace it with a real, short source-tree map of src/, plus a link to
            docs/backend-review-feature-roadmap.md.
          - Add a "Status" section that is honest and specific: what is verified green in CI,
            what is unit-tested only, and what is not built (billing, PDF export, self-host image).
          - Keep the existing "deterministic analysis, AI is optional and review-only" framing.

PHASE 1 — accuracy and trust (only after Phase 0 is green)

Task 1.1  tRPC is pinned to ^11.0.0-rc.364 — a release candidate — in a product intended for paid
          use. Upgrade all @trpc/* packages to the latest stable 11.x, fix the fallout, and confirm
          the verification command still passes. If the upgrade is not mechanically safe, stop and
          report rather than forcing it.

Task 1.2  Reconcile the marketing claims with the deployment. The landing page
          (src/app/page.tsx and src/components/marketing/*) implies near-instant analysis, but
          vercel.json only processes queued analyses via a daily 03:00 UTC cron. Choose one, and
          state the choice in the PR description:
            (a) Document the real latency and adjust copy to promise "a report", not a stopwatch
                figure, OR
            (b) Keep the speed claim only for the worker path, and make it conditional copy.
          Do not leave a number on the page that the deployed system cannot meet.

Task 1.3  pricing-section.tsx advertises a $15/month Teams tier. No billing code exists anywhere
          in the repo. Either (a) remove the dollar figure and present Teams as "in development,
          join the waitlist", or (b) leave it ONLY if a real billing integration lands in this
          same PR. Option (a) is the expected choice for this session. Never display a price the
          product cannot charge.

Task 1.4  Re-verify every number in README's Status section by running the commands, then write
          the true figures (test files, test count). Replace anything you cannot re-verify with a
          description rather than a count.

FINISH BY REPORTING, in the PR description:
  - the exact before/after output of the verification command
  - the typecheck diagnostic count before and after
  - which claims you removed or corrected, and why
  - anything you could not verify, labelled "unverified"
  - the two CI job names and their status

Do not start Phase 2 (PDF export, billing, features). Stop after Phase 1 and wait for a review.
```

---

## §2 — Environment contract (copy this when reviewing the PR)

Verified from `src/lib/env.ts`. Anything in a README or workflow that disagrees with this table is a bug.

**Required, no default — the app will not boot without them**

| Variable | Note |
|---|---|
| `DATABASE_URL` | Must parse as a URL |
| `REDIS_URL` | Must parse as a URL |
| `NEXTAUTH_SECRET` | Session encryption |
| `ENCRYPTION_SECRET` | Encrypts stored user AI provider keys; rotating it invalidates them |

**Optional, with defaults in code**

`GITHUB_CLIENT_ID` · `GITHUB_CLIENT_SECRET` · `GITHUB_WEBHOOK_SECRET` · `APP_URL` (defaults to `https://arborgit.vercel.app`) · `CRON_SECRET` · `CLONE_BASE_DIR` (`/tmp/arbor-clones`) · `CLONE_TIMEOUT` (60) · `MAX_REPO_SIZE_MB` (500) · `MAX_FILES` (5000) · `MAX_FILE_SIZE_KB` (100) · `MAX_PARSE_FILES` (2500) · `ANALYSIS_TIMEOUT_MS` (300000) · `ADMIN_EMAILS` · `ADMIN_GITHUB_USERNAMES` · `ADMIN_USERNAME` · `ADMIN_PASSWORD`

**Read outside `env.ts`** — must still be in `.env.example`

`RESEND_API_KEY` · `EMAIL_FROM` · `APP_TOKEN` · `SECRET_KEY` · `NEXT_PUBLIC_API_URL` · `NEXTAUTH_URL`

**Not environment variables.** AI providers are bring-your-own-key, stored encrypted per user in the database via `ENCRYPTION_SECRET`. There is no `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` env var — don't add one.

---

## §3 — Later phases (paste one at a time, after reviewing the previous PR)

### Phase 2 — make it sellable as a paid audit (fastest revenue)

```text
Continue in mdadeel/Arbor on a new branch feat/audit-report-export. The goal is to turn the
existing in-app report into a deliverable a consultant can sell: a branded PDF that is sent to a
client after an audit.

Task 2.1  Add a print route: app/(print)/report/[token]/page.tsx that renders the shared report
          (reuse getSharedReport from src/server/services/report-sharing.ts and the existing
          ProjectReport component) with a dedicated print stylesheet: A4 page size, cover page with
          repo name, commit SHA, scan date and policy version, then architecture summary, findings
          grouped by severity with file:line evidence, dependency risk, and a page footer with
          page numbers. Do not fork the data logic — reuse the existing query and service layer.

Task 2.2  Add scripts/export-report.ts that uses the already-installed Playwright to load that
          route with a valid share token and write a PDF to disk, with `npm run report:pdf -- <token>`
          wired in package.json. Include the run instructions in the README.

Task 2.3  Add a "Recommended actions" section to the report: the top 5 findings ranked by
          severity and blast radius, each with a one-line remediation and a rough effort estimate
          (S/M/L). Derive it deterministically from existing finding data — no AI call in this path.

Task 2.4  Add print-appropriate branding: Arbor logo, "Prepared for <client name>" if a client
          name is stored on the share link, and an invisible-ish footer noting the scan commit so a
          stale report is obvious.

Task 2.5  Acceptance: generate a real PDF from a real repository, confirm it is 6–10 pages, has no
          clipped tables or missing pages, and that every page footer shows the correct commit.
          Attach the PDF to the PR description. Add a test that the print route 404s on an expired
          or revoked token.
```

### Phase 3 — make it recurring revenue

```text
Continue in mdadeel/Arbor on branch feat/billing-and-worker. Two separate concerns, two commits.

Task 3.1  Billing. Integrate Paddle or Lemon Squeezy (both are merchant-of-record, which matters
          because the owner is in Bangladesh and Stripe does not support BD merchants). Requirements:
          - plans: Free, Teams (per workspace, not per seat)
          - checkout + billing portal behind a signed-in workspace owner
          - webhook handler that is idempotent and signature-verified, storing events so replays
            are safe
          - server-side plan limits enforced in the services layer, not only in the UI: analysis
            quota, workspace member count, scheduled scans
          - the pricing page must then display the real, chargeable price
          Do not gate existing free behaviour behind a paywall in this PR.

Task 3.2  Worker deployment. Analyses currently process via a daily Vercel cron. Add a Dockerfile
          for the app and a `worker` service to docker-compose so `src/worker/` can run as a
          long-lived process, and document deploying it to Fly.io or Railway with REDIS_URL pointing
          at the same instance. Keep the cron route as a documented fallback.

Task 3.3  Add a test that a second identical webhook delivery does not create a duplicate
          subscription change. Acceptance: `npm run typecheck && npm run lint && npm test -- --run && npm run build` all pass.
```

### Phase 4 — differentiation (the features buyers ask for)

```text
Continue in mdadeel/Arbor, one branch per item, in this order. Each must keep the verification
command green and must not slow a cold analysis by more than 20%.

  1. SARIF export — emit findings as valid SARIF 2.1.0 and add a documented upload path so
     GitHub Code Scanning shows Arbor findings in the Security tab. Validate against the schema.
  2. Hotspot analysis — churn from git log (simple-git is already a dependency) crossed with
     per-file complexity from the existing AST pass; render as a ranked table on the report.
  3. Ownership map — suggested CODEOWNERS from commit history, plus a bus-factor figure per
     top-level directory.
  4. Scan diff UI — "what changed since the previous scan" using the existing trend data.
  5. Self-hosted image — single Dockerfile with Postgres/Redis profiles, one documented
     `docker compose up` path, for buyers who cannot use a cloud service.
  6. CycloneDX — replace the current structural SBOM check with official schema validation.
```

---

## §4 — Corrections to the packaging files I staged earlier

Two errors in what I prepared in the previous step. **Fix these when you apply `chore/packaging`, or the build will fail.**

| File | Problem | Fix |
|---|---|---|
| `packaging/files/Arbor/.github/workflows/ci.yml` | Sets `GITHUB_ID` / `GITHUB_SECRET` (not the real names) and **omits `ENCRYPTION_SECRET`**, which is `z.string().min(1)` and therefore required | Use `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET`, and add `ENCRYPTION_SECRET` + `CRON_SECRET` placeholders |
| `packaging/files/Arbor/README.md` | Environment table lists `NEXTAUTH_URL`, `GITHUB_ID`, `GITHUB_SECRET`, `GITHUB_APP_ID`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` — none are the real contract (there is no GitHub App id in `env.ts`, and AI keys are BYOK in the DB, not env) | Replace with the §2 table |
| both | Neither includes `cp .env.example .env`, because the file doesn't exist | Create `.env.example` (Task 0.1) first, then the step becomes valid |

Rather than patching my staged copy, **let the other session produce the README and workflow from the real code** — that's Task 0.5 and 0.8 above, and it is why the master prompt tells it to read `src/lib/env.ts` first. If both branches exist, the other session's version wins and my staged Arbor files should be dropped.

---

## §5 — Definition of done

Phase 0 and 1 are complete when all of these are true, and the PR description proves each one:

- [ ] `npm ci && npx prisma generate && npx prisma validate && npm run typecheck && npm run lint && npm test -- --run && npm run build` passes locally and in CI
- [ ] Both CI jobs are green on the PR, and the badge in the README is uncommented only because of that
- [ ] `.env.example` exists and matches `src/lib/env.ts` exactly
- [ ] A fresh clone, following only the README, reaches a running app with a completed analysis
- [ ] No dead links in any markdown file
- [ ] `LICENSE` exists and the README has a licence section
- [ ] No price is displayed that the product cannot charge
- [ ] No claim is stated that was not verified by a command
