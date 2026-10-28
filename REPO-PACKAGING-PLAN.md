# Repo Packaging Plan — what we're doing, why, and in what order

**Status:** proposed · awaiting approval before execution
**Companion doc:** [`SELLING-AND-GROWTH-PLAN.md`](./SELLING-AND-GROWTH-PLAN.md) (the strategy and the evidence behind it)
**Owner:** Shahnawas Adeel (`@mdadeel`) · prepared 28 Oct 2026

---

## 1. What this work is

`SELLING-AND-GROWTH-PLAN.md` concluded that your code is already good enough to sell, but that **no repo on your account is packaged in a way a buyer can trust with money**. This plan fixes exactly that — and nothing else.

To be precise about scope: this is **presentation and infrastructure**, not product work. No new features, no refactors, no changes to application logic. Every task below either (a) adds metadata a buyer reads before opening the code, (b) adds automation that proves the code works, or (c) rewrites the words that currently undersell the work.

## 2. Goal

Make every public repo on `github.com/mdadeel` **legible to a buyer in under 60 seconds**: what it is, whether it runs, whether they're allowed to use it, and whether you're a person who ships.

### Success criteria (measurable, checked at the end)

| Metric | Now | Target |
|---|---|---|
| Repos with a description | 0 / 12 | 12 / 12 |
| Repos with a licence file | 1 / 12 (Preen) | 12 / 12 |
| Repos with a topic set (≥5 topics) | 2 / 12 | 12 / 12 |
| Repos with CI running typecheck/lint/test | 1 / 12 (`etuitionhub-frontend`) | 5 / 12 |
| Repos with a tagged release | 1 / 12 | 6 / 12 |
| Repos a stranger can run from the README | ~2 / 12 | 8 / 12 |
| Pinned repos that match your sales story | 0 | 6 |
| Profile README shows 4 projects + a hire-me CTA | No | Yes |
| Live demo links, verified working | Unknown | Verified or removed |

**Not** in the criteria: stars, followers, new features. Those follow from this, not the other way round.

## 3. Baseline (what I found, so we can prove improvement later)

| Repo | Description | Licence | Topics | CI | Release | README |
|---|---|---|---|---|---|---|
| Arbor | ✗ | ✗ | 0 | ✗ | ✗ | Good but contradicts product |
| etuitionhub-frontend | ✗ | ✗ | 0 | **✓ (3 workflows)** | ✗ | Strong; publishes demo creds |
| iehub-client | ✗ | ✗ | 0 | ✗ | ✗ | Decent, stale URL |
| iehub-server | ✗ | ✗ | 0 | ✗ | ✗ | **Empty** |
| Preen | ✓ | ✓ MIT | 10 | ✗ | ✓ v0.4.0 | Excellent |
| pinflow | ✗ | ✗ | 0 | ✗ | ✗ | Good, missing purpose |
| easyui | ✗ | ✗ | 0 | ✗ | ✗ | Says "nothing is built yet" |
| metro-optics | ✗ | ✗ | 0 | ✗ | ✗ | Student voice |
| ToyTopia | ✗ | ✗ | 5 | ✗ | ✗ | Self-deprecating |
| CodeArena-TeamProject (fork) | ✗ | ✗ | 0 | ✗ | ✗ | — |
| Doctoria (fork) | ✗ | ✗ | 0 | ✗ | ✗ | Fork — leave alone |
| mdadeel (profile) | stub | ✗ | 0 | ✗ | ✗ | Features 2 of 8 projects |

## 4. Five workstreams

### W1 — Metadata *(highest value, lowest risk, reversible)*
Descriptions, topics, homepage URLs, pinned repos. Applied directly to GitHub repo settings via the API. No commits, no branch changes, fully reversible, ~15 minutes.
Includes the exact target description and topic list for every repo in §5, for your approval.

### W2 — Licence and legal *(blocking; needs your decision)*
A repo with no licence cannot legally be bought, forked, or used by a client. This is the single most expensive omission on the account.

Because you intend to **sell** Arbor, e-TuitionBD and Import Export Hub, a blanket MIT licence would let any buyer resell them. See §6 for the recommendation and the decision I need from you. Delivered as a `LICENSE` file plus a one-paragraph "Commercial use" section in each README.

> **Correction after inspection:** `etuitionhub-frontend` already runs `test.yml`, `deploy.yml` and `react-doctor.yml`. It needs no new workflow — its README now links those badges instead. Everything below applies to the other repos.

### W3 — CI *(proves the code runs)*
GitHub Actions workflows, per repo, sized to what actually passes today:

| Repo | Workflow |
|---|---|
| Arbor | `prisma validate` → `typecheck` → `lint` → `test` → `build`, Node 20, Postgres + Redis services |
| etuitionhub-frontend | `lint` → `test` → `build`, Node 20 |
| Preen | pytest matrix 3.10–3.13 on Ubuntu 22.04/24.04, then build `.deb` + AppImage on tag |
| easyui | pnpm install → `lint` → `typecheck` → `test` → `build` |
| pinflow | ruff/pytest for backend, `npm run build` for `pinterest-web` |

Honest caveat: Arbor's own roadmap doc reports `typecheck` failing with 105 diagnostics, so its workflow will land **red** until that's fixed. I'll add it as a non-blocking job first (`continue-on-error`) so it reports without breaking anything, and flag the fix as separate product work. A badge that lies is worse than no badge.

### W4 — README rewrites
One template, applied consistently: one-line pitch → 3 screenshots → what it does (bullet, outcome-worded) → quick start that actually works → architecture (short) → status/roadmap honesty → licence.

Priority order:
1. `iehub-server` (empty → this is a whole product with no front door)
2. `easyui` (`docs/PLAN.md` says "nothing is built yet" while 36 components exist)
3. `metro-optics` (student voice → product voice)
4. `ToyTopia` (rewrite as a learning case study, or archive — your call)
5. `etuitionhub-frontend` (remove published demo credentials; state backend status honestly)
6. `pinflow` (lead with the problem, not the env vars)
7. `Arbor` (resolve the "no AI" vs "AI patch suggestions" contradiction)
8. Profile README (4 projects, hire-me CTA, drop the "philosophy" section)

### W5 — Portfolio surface
Pin the 6 repos that match the sales story; verify every live-demo URL and remove the dead ones; add `docs/` links from the profile; add a "Hire me for…" block with concrete offers and response time.

## 5. Per-repo target metadata (for approval)

| Repo | Proposed description | Proposed topics |
|---|---|---|
| **Arbor** | Architecture and health audits for GitHub repositories — interactive dependency maps, prioritised findings, PR checks and shareable reports. | `code-analysis` `architecture` `developer-tools` `static-analysis` `codebase-visualization` `nextjs` `typescript` `trpc` `prisma` `software-quality` |
| **etuitionhub-frontend** | Tuition marketplace and coaching-centre portal: role dashboards, realtime chat, WebRTC classrooms and bKash/Nagad checkout. | `edtech` `react` `vite` `marketplace` `bangladesh` `socket-io` `webrtc` `tailwindcss` `education` `saas` |
| **iehub-client** | Client for a B2B import/export platform: verified organisations, product catalogue, RFQs, disputes and document tracking. | `b2b` `import-export` `trade` `react` `firebase` `logistics` `marketplace` `bangladesh` |
| **iehub-server** | Express/MongoDB API for a B2B trade platform: multi-organisation tenancy, RBAC, RFQs, disputes, documents, webhooks and audit logs. | `nodejs` `express` `mongodb` `rbac` `rest-api` `b2b` `trade` `logistics` `webhooks` |
| **Preen** | *(keep existing)* System setup, deep cleaning and tuning for Linux — GTK 3 app with a simulate-before-you-act switch. | *(keep 10, add `pygobject`, `ubuntu`)* |
| **pinflow** | AI-assisted Pinterest scheduling: vision-generated metadata, bulk CSV upload, calendar, queue and performance analytics. | `pinterest` `automation` `scheduling` `python` `fastapi` `nextjs` `content-marketing` `ai` |
| **easyui** | Accessible React component library with runtime design-token theming — change accent, radius and font without touching component code. | `react` `ui-components` `design-system` `design-tokens` `accessibility` `typescript` `tailwindcss` |
| **metro-optics** | Eyewear storefront with prescription management, live inventory and an admin dashboard. React 19 + Firebase. | `ecommerce` `react` `firebase` `tailwindcss` `storefront` `prescriptions` |
| **ToyTopia** | Early React/Firebase learning project — second-hand toy marketplace with auth, search and admin CRUD. | *(keep 5)* |
| **mdadeel** | Profile README. | `profile-readme` |
| Forks (CodeArena, Doctoria) | Leave untouched | — |

## 6. The decision I need: licensing

Three of your repos are products you want to charge for. The licence determines whether a buyer can legally resell them.

| Option | What it means | Fits |
|---|---|---|
| **A. Proprietary, source-available** — `All rights reserved`, public read-only, commercial licence on request | Maximum control. Clients can read but not redistribute. Standard for consultancies selling implementations. | Arbor, e-TuitionBD, iehub |
| **B. AGPL-3.0 + commercial dual licence** | Public can self-host for personal use; anyone offering it as a service must publish changes or buy your commercial licence. Best of both: visible code, protected market. | Arbor, pinflow |
| **C. MIT** | Anyone can use, fork and resell, including competitors. Great for libraries and credibility, fatal for products. | easyui, Preen (already), metro-optics |
| **D. Leave unlicensed** | Nobody may legally use or buy it. | none |

**My recommendation:** **A** for e-TuitionBD and iehub (you sell bespoke implementations, so control matters and openness adds little), **B** for Arbor (a developer tool needs stars and community to get distribution, and AGPL is the standard defence for open-source-then-SaaS), **C** for easyui, metro-optics, ToyTopia, and keep MIT on Preen.

## 7. Execution order

| Step | Workstream | Time | Needs you? |
|---|---|---|---|
| 1 | W1 metadata on all 12 repos | ~15 min | Approval of §5 |
| 2 | W2 `LICENSE` + commercial-use section | ~30 min | Decision in §6 |
| 3 | W3 CI for the 5 runnable repos | ~60 min | Nothing |
| 4 | W4 README rewrites, in the order above | ~2 h | Screenshots (see §9) |
| 5 | W5 pin repos, verify demos, profile README | ~30 min | Confirm live URLs work |
| 6 | Verify: re-run the §2 checks, report deltas | ~15 min | Nothing |

Total: roughly half a day of work, done incrementally. After that I'll re-audit and tell you exactly what changed.

## 8. What I will not do without explicit instruction

- **Not** change any application logic, refactor code, or "fix" the 105 type errors — that's product work and belongs in its own plan.
- **Not** delete, archive or make private any repo. If ToyTopia should go, you do it or tell me explicitly.
- **Not** publish, expose or rotate any secret, and not touch a `.env` file.
- **Not** publish the `etuitionhub-backend` repo — that's your call, and if you'd rather not, we ship an OpenAPI contract instead so buyers still get a contract they can build against.
- **Not** claim a workflow passes unless I've seen it pass.

## 9. What I need from you

1. **Approval of the licence policy in §6** (or an override).
2. **Screenshots.** I can't record your running apps. For each repo I'll leave a clearly-marked placeholder block; you drop 2–3 PNGs/GIFs into `docs/screenshots/` and the README picks them up. Without images, README quality caps out around 70%.
3. **Live URL confirmation.** From this sandbox I can only reach GitHub/npm/PyPI, so I couldn't verify `arborgit.vercel.app`, `e-tuitionhub.vercel.app`, `iehub.vercel.app`, `metro-optics.vercel.app`, `toy-topia-ashy.vercel.app` or `mdadeel.me`. Open them; I'll keep the working ones and remove the rest rather than ship dead links.
4. **One-line confirmation on ToyTopia:** rewrite or archive.
5. **A decision on `etuitionhub-backend`:** publish it, or ship an OpenAPI contract?

## 10. A note on how the changes will land

GitHub repo metadata (description, topics, homepage, pins) is **repo settings, not code** — I apply it directly through the API and it creates no commits or branches.

File changes in *other* repos (READMEs, `LICENSE`, `.github/workflows/*`) are a different matter: this session is bound to the `arena/57bde536-mdadeel` branch, so I won't push branches into your other repositories. Instead I'll produce every file here, under `packaging/<repo>/`, together with a single reviewed script (`packaging/apply.sh`) that commits them to the right repos via the GitHub Contents API. You run it when you're happy — one command, fully visible, nothing hidden.

So the deliverable is: **metadata applied live, files staged and reviewable, one command to publish them.**

---

## 11. Definition of done

- Every repo answers, in this order and within one screen: *what is this, what does it look like, how do I run it, what am I allowed to do with it.*
- CI badges are green or absent — never green when red.
- No live link on the account 404s.
- A stranger can clone 8 of the 12 and have the app running in under 10 minutes.
- Your profile makes the four sellable projects obvious and offers a specific way to hire you.
- `SELLING-AND-GROWTH-PLAN.md` §7's checklist is fully ticked, and we can prove it against §3.


---

## Appendix — execution log (28 Oct 2026)

### Status

| Workstream | Status | Where |
|---|---|---|
| W1 metadata | **Blocked** — needs your `gh` session | `packaging/metadata.sh` (tested, dry-run works) |
| W2 licences | **Staged** | `packaging/files/*/LICENSE` + `packaging/licenses/` |
| W3 CI | **Staged** — YAML validated, 8 new workflows | `packaging/files/*/.github/workflows/ci.yml` |
| W4 READMEs | **Staged** — 7 rewritten from the code | `packaging/files/*/README.md` |
| W4 profile README | **Done — committed to this branch** | `README.md` |
| W5 pin + demos | Manual (pins) / confirmed by you (links) | see `packaging/README.md` |

### Why W1 is blocked, not done

The GitHub integration in this session has read access and content write, but **not repository administration**:

```
PATCH /repos/mdadeel/Arbor      → 403 Resource not accessible by integration
PUT   /repos/mdadeel/Arbor/topics → 403
GraphQL updateTopics            → FORBIDDEN
```

Descriptions and topics therefore have to be applied by a session holding your admin rights. `packaging/metadata.sh` does exactly that — dry-run first, then apply — and it verifies admin access per repo before touching anything.

For the same reason, file changes are delivered as staged files plus `packaging/apply-files.sh`, which branches, commits, pushes and opens one PR per repo. Nothing lands on `main` unreviewed.

### What was actually verified vs. assumed

- **Verified:** Preen's test command — ran `pip install -e .` + `pytest` locally: **69 passed, 1 skipped**. All 9 workflow files parse as valid YAML with the expected job counts. Every licence text was fetched from the SPDX canonical source.
- **Assumed:** that the other workflows pass on first run. They probably won't. Every badge is therefore commented out with an instruction to enable it only after a green run.
- **Not done:** screenshots (I can't run your apps), pins (your account UI), and the private backend repo (`etuitionhub--backend` is not accessible to the integration — its files are staged for you).

### Corrections to §3 and to the growth plan

1. **CI baseline was wrong.** It is 1/12, not 0/12: `etuitionhub-frontend` already runs lint + unit tests + a Playwright e2e against the deployed URL, plus a prebuilt Vercel deploy and a PR health check. That repo is the template for the others, not a gap.
2. **The e-TuitionBD backend is a bigger product than assumed.** Enumerating every request the client makes (`370` call sites) reveals an institution platform: organisations, branches, courses, batches, enrollments, guardians, attendance, exams and results publishing, staff roles and salaries, invoices, per-tenant subscriptions, wallet and payouts, an assignment lifecycle, and a full AI teaching suite. Sell it as an institute management system; the marketplace is the acquisition hook, not the product.
3. **Licence decision as approved:** AGPL-3.0 for Arbor and pinflow (dual-licensed), PROPRIETARY for e-TuitionBD (both repos) and both iehub repos, MIT for easyui, metro-optics, and Preen unchanged.
4. **ToyTopia and both forks untouched**, per your instruction.
