# Packaging — runbook

Everything needed to execute [`../REPO-PACKAGING-PLAN.md`](../REPO-PACKAGING-PLAN.md). One command per workstream, nothing lands on `main` unreviewed.

```
packaging/
├── README.md                 ← you are here
├── metadata.sh               W1  descriptions + topics for every repo
├── apply-files.sh            W2/W3/W4  LICENSE + README + CI, as PRs
├── verify.sh                 W5  re-check the success criteria
├── licenses/                 AGPL-3.0, MIT, PROPRIETARY
└── files/<repo>/             staged LICENSE, README.md, .github/workflows/ci.yml
```

---

## Why you have to run these, not me

The GitHub integration available in this session has **read access plus content write via git**, but **not repository administration**. Concretely:

- `PATCH /repos/{owner}/{repo}` → `403 Resource not accessible by integration`
- `PUT /repos/{owner}/{repo}/topics` → same
- GraphQL `updateTopics` → same

So descriptions and topics can't be applied from here, and for the same class of reason I'm not pushing branches into your other repositories from this session. The scripts in this directory run with **your** `gh` credentials, which do have admin rights, and they show you every change before it happens.

`mdadeel/etuitionhub--backend` is **private** and not accessible to the integration at all — its staged files are ready in `files/etuitionhub--backend/` and will be skipped automatically; apply them when you have that repo checked out locally.

---

## Order of operations

### 0. Preflight

```bash
gh auth status          # must be logged in as mdadeel
gh auth refresh -s admin:public_key 2>/dev/null || true   # only if a step reports 403
```

### 1. W1 — Metadata (fastest, safest, reversible)

```bash
cd packaging
./metadata.sh --dry-run      # read it first; nothing changes
./metadata.sh                # apply
./metadata.sh Arbor          # or a single repo
```

Sets a description and 5–12 topics on 10 repos. Leaves `ToyTopia` (your call: skip until upgraded), both forks, and the private backend alone.

**Rollback:** each value is one API call; clear a description with `gh api -X PATCH repos/mdadeel/<repo> -f description=""` and topics with `-f names='[]'`.

### 2. W2/W3/W4 — Files, as pull requests

```bash
./apply-files.sh --dry-run              # see every file and its diff size
./apply-files.sh                        # all repos → branch chore/packaging + PR
./apply-files.sh Arbor Preen            # just these
./apply-files.sh --no-pr                # push the branch only
```

Per repo it clones, branches, copies the staged files, commits, pushes, and opens a PR titled *“Packaging: licence, README and CI”*. Nothing touches `main` until you merge.

**Rollback:** delete the branch and PR — `gh pr close <n> --repo mdadeel/<repo> --delete-branch`.

### 3. W5 — Verify

```bash
./verify.sh
```

Prints a per-repo table and the totals against the plan's targets. Run it before and after; that's the evidence.

### 4. Pinning (manual, 30 seconds)

**Profile → Customize your pins**, pin in this order:
`Arbor` · `etuitionhub-frontend` · `iehub-server` · `Preen` · `easyui` · `pinflow`

---

## What each staged file assumes

| Repo | Licence | CI | Notes |
|---|---|---|---|
| Arbor | AGPL-3.0 | typecheck¹, lint, test, build² | Postgres + Redis services; `prisma validate` + `migrate deploy` |
| etuitionhub-frontend | PROPRIETARY | **already had CI** — README now links `test.yml`/`deploy.yml` badges | No new workflow added: it would have duplicated `test.yml` |
| etuitionhub--backend | PROPRIETARY | parse-only + `npm test --if-present` | Private repo; README carries `TODO (owner)` markers for env/scripts I could not read |
| iehub-server | PROPRIETARY | `node --check` + env-guard assertion | No test suite exists yet, so no fake test step |
| iehub-client | PROPRIETARY | lint + build | Test suite to be added later |
| easyui | MIT | pnpm lint → typecheck → test → build | 38 test files already exist |
| Preen | *(MIT, kept)* | **verified locally**: 69 passed, 1 skipped | Matrix 3.10–3.13 × Ubuntu 22.04/24.04; `python -m build` artifacts |
| pinflow | AGPL-3.0 | backend ruff+pytest³, web test+build | ruff/pytest non-blocking until findings are cleared |
| metro-optics | MIT | lint + build | — |
| ToyTopia | — | — | Not touched, per your instruction |

¹ Typecheck is `continue-on-error: true`: the roadmap documents outstanding diagnostics, so a red step is expected until that is fixed.
² Build is `continue-on-error: true` for the same reason.
³ Non-blocking for the same reason.

**The badges are commented out in every README.** Enable a badge only after the workflow has run green at least once — a badge that lies is worse than no badge. The plan (§11) commits to this.

### Verified vs. unverified

| Claim | Status |
|---|---|
| Preen's test command | **Verified** — ran it: 69 passed, 1 skipped |
| All 9 workflow files are valid YAML with resolvable actions | **Verified** — parsed and job-counted |
| `node --check` passes on every `iehub-server` file | Not run here (needs `npm ci`) |
| Arbor lint/test pass in CI | Not verified — reported passing locally, but 105 typecheck diagnostics remain |
| Workflows will pass on first run | **Assume not.** Expect to iterate 1–2 rounds; that's normal, and it's why the badges are off |

---

## Screenshots — what I need from you

I can't run your apps from this sandbox, so every README has a commented placeholder near the top:

```md
<!-- SCREENSHOT: replace this block with 2–3 images ... docs/screenshots/ -->
```

For each repo, capture and save under `docs/screenshots/`:

| Repo | Capture |
|---|---|
| Arbor | architecture graph, findings list, project dashboard |
| etuitionhub-frontend | home, tutor search with filters, tutor dashboard |
| etuitionhub--backend | — (no UI) |
| iehub-client | landing, product catalogue, organisation dashboard |
| iehub-server | — (no UI) |
| easyui | playground with two different accents side by side |
| pinflow | calendar, queue, pin detail |
| metro-optics | shop grid, product detail, admin |
| Preen | dashboard, deep-clean scan with sizes |

Then either send them to me, or un-comment the `<p align="center">…</p>` block and fix the paths. A GIF beats three PNGs for anything with motion (Arbor's graph, Preen's scan).

---

## Corrections to the earlier audit

Two things in `SELLING-AND-GROWTH-PLAN.md` were wrong, and are corrected here:

1. **“0 of 12 repos have CI” → actually 1.** `etuitionhub-frontend` already runs three workflows: `test.yml` (lint + unit + Playwright e2e against the live URL), `deploy.yml` (Vercel prebuilt deploy) and `react-doctor.yml`. That repo is not a gap — it's the model for the others. The corrected baseline is CI **1/10**, not 0/12.
2. **The e-TuitionBD backend is much bigger than its frontend implies.** Reading every request the client makes shows an institution platform, not just a marketplace: organisations, branches, courses, batches, enrollments, guardians, attendance, exams and results publishing, staff roles and salaries, invoices, per-tenant subscription plans, wallet and withdrawal approvals, an assignment lifecycle, a full AI teaching suite (lesson plans, curriculum mapping, quiz generation and marking, notes, streaming chat, usage tracking), moderation, impersonation and audit logs. Its staged README documents all of it. This is a **stronger white-label product than the plan assumed** — sell it to coaching centres and schools as an institute management system, with the marketplace as a bonus feature.

Both corrections are reflected in the staged files and in §7 of the packaging plan.

---

## Definition of done

```bash
./verify.sh
```

...shows descriptions 10/10, licences 10/10, topics ≥5 10/10, CI ≥5, releases ≥1, plus: no 404 links, at least four repos with screenshots, and six pins that match the story.
