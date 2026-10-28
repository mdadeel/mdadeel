# What You Can Actually Sell — GitHub Audit & Growth Plan

**Account:** [github.com/mdadeel](https://github.com/mdadeel) · 12 public repos · prepared 28 Oct 2026
**Method:** every claim below comes from reading the code, schema, tests, packaging and README in your repos — not from the README marketing copy. Line counts, test counts and file paths are real.

---

## 0. The one-paragraph answer

You have **one genuinely sellable product (Arbor)**, **two sellable B2B platforms (e-TuitionBD and Import Export Hub)** if you reposition them, **one strong credibility asset (Preen)**, and **four things you should not try to sell** (easyui in its current name, pinflow under its current model, metro-optics as a product, ToyTopia at all).

The problem is **not** your code. The problem is that **none of your repos are packaged as something a buyer can trust with money**: 0 of 12 have a description, 1 of 12 has a licence, 0 have CI, 0 have a release except Preen, and the one repo with a pricing page ($15/mo Teams) has no billing code behind it. Fix the packaging and roughly $600–$3,000/month of realistic income is reachable in 90 days — mostly from **productized services first, SaaS second**.

---

## 1. Scorecard

| Repo | What it *actually* is (from code) | Proof of substance | Sell it? | To whom | Model |
|---|---|---|---|---|---|
| **Arbor** | Architecture/health audit platform for GitHub repos. Next.js 15, tRPC, Prisma (28 models), BullMQ, workspace RBAC, PR check runs, SBOM, AI patch suggestions | 41k LOC TS, 265 src files, **52 test files / 259 passing tests**, 9 migrations, waitlist + share links + audit log | ✅ **Yes — flagship** | Agencies, CTOs, VCs doing technical due diligence, dev teams | Productized audit → team SaaS |
| **e-TuitionBD** | Full tuition marketplace: 3 role dashboards, realtime chat, WebRTC rooms, bKash/Nagad/Rocket payment UI, i18n, PWA | **65.5k LOC**, 39 deps, 29 test files, sitemap/OG/SEO render, admin finance workspace | ✅ Yes, **repackaged** | Coaching centres, schools, tutoring chains | White-label licence + setup |
| **Import Export Hub** (iehub-client + server) | B2B trade platform: organisations, members, RFQ, disputes, documents, audit log, webhooks | 6.1k LOC server (Express/Mongoose) + React client, org/role middleware, rate limiter, env validation | ✅ Yes, **highest ticket** | Export houses & freight forwarders in Ctg / EPZ | Implementation + retainer |
| **Preen** | GTK3 Linux maintenance app: install/remove, deep clean with size preview, systemd, swap/ZRAM, simulate mode | 6.7k LOC Python, **70 tests**, MIT, v0.4.0 release, .deb + AppImage packaging | ⚠️ Credibility asset, weak revenue | Linux users, distros, IT support shops | Sponsorship / Pro build |
| **pinflow** | Pinterest automation: AI vision metadata, scheduler, calendar, queue, analytics | 6k LOC Python + Next.js, sidecar, ENTERPRISE_PLAN self-scored 6.5/10 | ⚠️ Only after a pivot | Etsy/POD sellers, social SMBs | Subscription (with ToS risk) |
| **easyui** | 36-component React UI library, token pipeline, theming playground | 38 test files, monorepo, tokens→CSS pipeline | ❌ Not until renamed | — | — |
| **metro-optics** | Eyewear storefront, React 19 + Firebase, admin | 138 src files | ⚠️ As a build service / template | Local optics retailers, agencies | Fixed-price build |
| **ToyTopia** | Early learning MERN toy shop | small | ❌ Archive or rewrite | — | — |

> Note: I could not load your live demos from this sandbox (network is restricted to GitHub/npm/PyPI), so verify each URL in a browser before you put it in front of a client. `vercel.json` in e-TuitionBD rewrites `/api/*` to `etuitionhub-backend.vercel.app`, and **that backend repo is not public** — that is the single biggest trust problem on your account right now.

---

## 2. Arbor — your flagship, and the only one with a real market

### What you already built (and it's a lot)
- 28 Prisma models: `Project`, `Analysis`, `Workspace`, `WorkspaceMember`, `PolicyPackSetting`, `FindingTriage`, `ScanSchedule`, `ReportShareLink`, `PatchSuggestion`, `GitHubWebhookDelivery`, `PullRequestAnalysis`, `Notification`, `AuditLog`.
- Deterministic AST analysis (Babel parser/traverse + dagre for graph layout), graph canvas, health dashboards, env-var inventory, API spec parsing, docs hub, commit/contributor timelines, SBOM export, GitHub webhook + Check Run publishing, admin panel with impersonation and audit.
- `src/app/share/[token]/page.tsx` + `ReportShareLink` = **you can already generate a shareable, expiring report link.** Most people never build this. It is the key to selling audits.

### What's blocking revenue (straight from `docs/backend-review-feature-roadmap.md`)
That doc is unusually honest and it's also your to-do list:
- **No phase is release-complete.** Phase 0 auth hardening, Phase 1 PR checks, Phase 2 policy packs, Phase 3 trends/notifications, Phase 4 SBOM, Phase 5 AI patches — all "code present, not verified."
- `npm run typecheck` **fails with 105 diagnostics**; `npm run build` unverified; Prisma client never generated cleanly in that environment.
- **No CI at all** (`.github/` doesn't exist). No licence, no description, no topics, no release tag.
- Landing page sells **"$15/month Teams"** while there is **zero Stripe/billing code** in the repo. Charging is not wired. Do not put a price on a page you can't bill.
- Pricing copy contradicts itself: README says *"no AI"*, later phases add OpenAI/Anthropic providers.

### How to sell it — three paths, in order of speed

**Path A (start this week): productized "Codebase Due-Diligence Audit" — $299–$999 per report**
This is the fastest money and it fits your product exactly.
- Buyer: (1) agencies/studios inheriting a legacy codebase, (2) founders buying or investing in a software company, (3) CTOs onboarding a team.
- Deliverable: connect repo → run Arbor → export a 6–10 page PDF (architecture map, module coupling, hotspots, secret/leak findings, dependency risk, top 5 prioritised fixes, 30-day remediation plan) → give a 45-min call.
- Why it works: the buyer is spending $50k–$500k on a decision; $750 for a technical opinion is trivially cheap. And you already have the share-link mechanism to deliver it.
- What you need: a **PDF export** (Playwright print of the share page — you already have Playwright as a dep), 3 **anonymised sample reports**, and a landing page section on arborgit.vercel.app.

**Path B (30–60 days): Arbor for agencies — $49–$149/team/month**
Small dev shops want to show clients "here's the health of the system we're maintaining." Sell **per workspace, not per seat**, unlimited repos, scheduled scans, white-label share links (your brand → their brand), PDF export.
- You need: Stripe/Paddle billing, workspace-level plan limits, and the Phase 3 scheduled-scan + share-link work that is already coded but unverified.

**Path C (60–90 days): GitHub Marketplace app**
The moment you have a GitHub App with Check Runs (Phase 1, already coded), you can list on GitHub Marketplace and get distribution from developers already looking for this. This is the only path with free inbound traffic.

### Feature upgrades that make it more sellable

**Must-have before charging (P0)**
1. CI: GitHub Actions running `typecheck`, `lint`, `test`, `build`, `prisma validate` on every PR. Add the badge to the README — buyers read badges.
2. Fix the 105 type errors and get one clean `npm run build`. Nobody pays for "unverified."
3. Real billing (Paddle/Lemon Squeezy — see §6) **or** delete the $15 price.
4. Sentry + structured logging + a status/limits page. A paid tool that silently fails is a refund.

**Industry-standard features buyers will ask for (P1)**
5. **SARIF export** → upload findings to GitHub Code Scanning so they appear in the Security tab. Cheap to add (you already produce structured findings), enormous perceived value.
6. **Hotspot analysis**: churn (git log) × complexity per file — the CodeScene "hotspot" view. You already read `simple-git` history and AST complexity, so this is mostly UI.
7. **Ownership map**: suggested CODEOWNERS from commit history, bus-factor per directory. This is what CTOs actually fear.
8. **Scan diff / "what changed since last scan"** view — the `Trend` work covers data, it needs a UI. This is what makes it a *subscription* instead of a one-off.
9. **Self-hosted Docker image.** In Bangladesh (and any bank/telco/gov client), a cloud-only tool is unsellable. One `docker compose up` line = an entirely new market, and you already have `docker-compose.yml`.
10. **Official CycloneDX schema validation** (your own doc admits it's custom structural checking). One library swap.
11. **Monorepo support** — workspaces/pnpm/turborepo detection with per-package graphs.

**Differentiators users will ask for after they're paying (P2)**
12. Onboarding-doc generation from the actual graph ("start here" reading order for new hires).
13. Benchmark: "your repo vs 200 similar repos" percentile — cheap survey data, high perceived value.
14. Test-gap map: which modules have zero test coverage, from import graph + test file matching.
15. Public "architecture card" badge (you have `api/badge/[identifier]`) that links back to Arbor — free distribution, like Shields.io.
16. Slack/Teams digest of weekly health deltas.

### Risks
- Crowded category (CodeScene, SonarQube, CodeRabbit, Graphite, CodeSee). **Do not compete on "AI reviews".** Compete on *understanding* — maps + onboarding + due diligence. That's the one thing your architecture graph does that linters don't.
- Your repos are 0-star. That is a distribution problem, not a code problem — a dev tool with no users doesn't get bought. Path A (services) generates case studies, which is how dev tools actually start.

---

## 3. e-TuitionBD — sell it B2B as white-label, not B2C as a marketplace

### What's there
65.5k LOC React 19 + Vite, 39 deps, 29 test files. Real depth: role-aware dashboards (student/tutor/admin), Socket.IO chat with read receipts and typing, `simple-peer` WebRTC session rooms, bKash/Nagad/Rocket/Bank checkout, tutor verification with document upload, admin finance + withdrawals + audit logs, i18n (`src/i18n.js`, locales), PWA plugin, SEO render endpoint, sitemap/robots/llms.txt, `X-Frame-Options`/HSTS/CSP-ish headers. This is more complete than most "production-ready" portfolio projects.

### What's blocking revenue
1. **The backend is not in your GitHub.** `vercel.json` proxies to `etuitionhub-backend.vercel.app`, but there is no such public repo. Any client, agency, or buyer will notice in 30 seconds.
2. **Demo credentials are published in the README.** Fine for a demo, fatal for a paying client's tenant. Gate them or remove them.
3. Payment flows reference `mockData` in places (`Checkout.jsx`, `PayPanel.jsx`) — audit which paths hit the real backend and which are UI-only, and say so out loud in the README.
4. p2p WebRTC will fail behind CGNAT/mobile networks without a TURN server. Either run coturn (cost: ~$5/mo) or offer Jitsi fallback — otherwise your "video classes" demo breaks on Bangladeshi mobile data, which is exactly your buyer's network.

### How to sell it
**Do not sell a consumer marketplace.** Two-sided marketplaces need marketing spend you don't have. Sell the *software* to whoever already has the students:

| Buyer | Pitch | Price (realistic) |
|---|---|---|
| Coaching centres / batch-based tuition centres | "Your own branded portal: batches, attendance, results, fees, parent SMS, online classes" | ৳60,000–150,000 setup + ৳5,000–12,000/mo |
| Schools (English version / Cambridge) | "Tutor directory + class scheduling + parent portal" | ৳150,000–400,000 |
| Tutor associations / chains | Multi-branch tenancy | ৳200,000+ |

**Delivery model:** one codebase, one deploy per client (Vercel + custom domain), branding via env/config, data isolated per tenant. Multi-tenant isolation already exists conceptually — make it explicit (tenant id on every query, tested).

### Feature upgrades — the ones institutions actually pay for
**P0**
1. Make the backend public (or a documented "API contract" OpenAPI spec + Postman collection). Trust.
2. Fee invoice + **bKash/Nagad payment verification with server-side callback + idempotency + refund ledger**. Institutions will not use a payment screen they don't trust.
3. Attendance + batch/class scheduling with conflict detection. This is the #1 requested feature in every coaching-centre system.
4. Parent portal + **SMS via a local gateway** (SSL Wireless / BulkSMSBD / Robi). Email is not read in Bangladesh; SMS is. This single feature closes deals.
5. Exam/result publishing with grade sheets and printable marksheets.

**P1**
6. Tutor payout ledger with hold period, commission rules, and downloadable statements (you have withdrawals admin already).
7. Bangla-first UI (i18n exists — finish the locale) and a **low-bandwidth mode** (defer images, list view) — your users are on 3G and cheap Androids.
8. Offline-first PWA for attendance taking.
9. WhatsApp notifications (Cloud API) — where parents actually are.
10. Calendar sync (ICS export), plus a public booking page (you have `PublicBookingPage.jsx` — polish it, it's a differentiator).

**P2**
11. White-label admin theme builder, custom domain onboarding, and a super-admin console for you to manage all client deployments.
12. Mobile app wrapper (Capacitor) if a client asks; PWA first.
13. Institute-level analytics: retention, revenue per batch, tutor utilisation.

### Risks
- Market is crowded locally (10 Minute School, Bikroy tutors, Shikho) and consumer CAC is brutal. **B2B avoids all of that.**
- Your current pricing model (escrow split commission) requires payment-aggregator licensing conversations in BD. Swap to **subscription + per-institution invoicing** and the compliance headache disappears.

---

## 4. Import Export Hub (iehub) — your highest-ticket, most under-sold asset

### What's there
Server (6.1k LOC Express/Mongoose) with `Organization`, `OrganizationMember`, `Invite`, `RFQ`, `Dispute`, `Document`, `AuditLog`, `WebhookSubscription`, `CompanyProfile`, `Import`, `Product`; middleware for auth, per-permission checks, correlation IDs, rate limiting, org resolution, env validation. 12 route modules including analytics and SEO. The client already has org directory, org details, RFQ flows.

**This is a real B2B SaaS skeleton.** And you live in **Chattogram — the port city**. Bangladesh's export economy runs through your postal code. This is the project I'd sell hardest if I were you.

### What's blocking revenue
1. No description, no licence, no topics, no docs on how to run it end-to-end. `iehub-server` has an **empty README**.
2. No tests anywhere in the server.
3. No document generation (invoices/LC paperwork) — the thing exporters actually pay for.

### How to sell it
Target buyers in this order:
1. **Export houses / buying houses in Chattogram & Dhaka** (garments, leather, jute, frozen fish, agro). Pitch: "Your own buyer portal + RFQ management + shipment document tracker."
2. **Freight forwarders / C&F agents** — they live in email and Excel; a document checklist tracker is an easy yes.
3. **Chamber / trade association** — a member directory + verified buyer/seller marketplace (charge members, the association pays you).
4. **EPZ enterprises** — procurement + supplier onboarding.

| Package | Scope | Price |
|---|---|---|
| Pilot | Single org, product catalogue, RFQ, document tracker, branded | ৳150,000–250,000 |
| Full | Multi-org, roles, disputes, audit, webhooks, buyer portal | ৳400,000–800,000 |
| Retainer | Hosting, support, changes | ৳15,000–40,000/mo |

Sell the pilot first, always. Never quote the full build to a first client.

### Feature upgrades — what makes it industry-friendly
**P0**
1. Write a real README + seed script + Postman collection. You cannot sell what a client's IT guy can't run.
2. Tests for auth/permission middleware (the crown jewels).
3. **Document generation**: Proforma Invoice, Commercial Invoice, Packing List, Certificate of Origin tracking, **LC (Letter of Credit) module** with amendment history and expiry alerts. Exporters' lives are documents; this is the whole product.
4. Document checklist per shipment (which docs are required for which destination/incoterm) with status and reminders.
5. Email + WhatsApp notifications on RFQ and document deadlines.

**P1**
6. **HS code classification** assist (searchable HS database + AI suggestion, human-confirmed) — mandatory for customs and a strong differentiator.
7. **Incoterms 2020 calculator** (FOB/CIF/CFR/ex-works) and landed-cost/duty estimator with BDT FX rates.
8. Buyer/supplier verification (KYC lite): trade licence, TIN/BIN, bank reference, uploaded docs, verification badge.
9. Shipment tracking (BL/container number, milestones) with a public tracking page for buyers.
10. Bulk CSV/Excel import of products and buyers — every exporter has 4,000 rows in Excel and will judge you on this.
11. Audit log UI (data exists) + role management UI.
12. Public SEO catalogue (you already have `seoRoutes.js`) — free organic acquisition for the *client*, which is an easy selling point.

**P2**
13. Marketplace/discovery layer between verified buyers and sellers (only after you have 20 paying orgs).
14. Financing/invoice-discounting referral module (banks pay for qualified leads).
15. Multi-currency + FX hedging notes, and integration with a customs broker's API if one opens up.

### Risks
- Fragmented buying, long sales cycles, and trust barriers. Mitigate with a **free 3-month pilot for one known export house** (you're in Ctg — go to the Agrabad C&F agent offices and the Chamber) in exchange for a testimonial and a logo.
- Don't build a marketplace first. Ship the boring document/RFQ workflow, it's what gets invoices paid.

---

## 5. Preen — best-crafted repo, weakest revenue. Use it as a door-opener.

### What's there
6.7k LOC Python/GTK3, **70 tests**, MIT licence, proper `pyproject.toml`, Debian packaging (`debian/control`, `rules`, `install`, changelog), `packaging/build_appimage.sh`, `build_deb.sh`, docs (ARCHITECTURE, USER_GUIDE, CONTRIBUTING, CHANGELOG, ROAST), **7 stars, 1 fork, v0.4.0 released**, 10 topics. This is your most *professionally packaged* repo by far — which is ironic, because it's the least monetisable.

### What's blocking
- **No CI** despite a `docs/ci-workflow.yml.example` sitting there unused.
- **`preen` on PyPI is already taken** (`preen` 0.8.0 by another author) — you cannot `pip install preen`. You'll need `preen-tool` / `zorin-preen` on PyPI, or distribute only via .deb/AppImage/Flathub.
- `gui.py` is **2,580 lines in one file** — refactor into pages, or contributors won't touch it.
- Not on Flathub. Not on AUR. No i18n.

### How to make it earn
Realistically: **it won't be a product business.** Use it three ways:
1. **Credibility asset** — the repo that proves you ship polished, tested, packaged software. It's the first thing to link in a proposal to a Linux/OEM client. Keep it excellent.
2. **Sponsorship funnel** — GitHub Sponsors / Polar.sh with a "Preen Pro" build: config profiles export/import, auto-snapshot before changes, priority builds for ARM/other distros. ৳1,000–2,000 one-time. Even 20 buyers = meaningful, and sponsorships are recurring.
3. **B2B door-opener** — pitch "we'll build and package your Linux desktop utility with AppImage/deb/Flatpak + CI + tests" to distros, hardware vendors, or ISVs. Preen *is* the portfolio for that service. Price ৳80,000–250,000 per app.

### Upgrades worth doing (they double as portfolio proof)
1. GitHub Actions matrix (3.8–3.13, Ubuntu 22.04/24.04), build .deb + AppImage artifacts on tag → this is the missing `.example` file, just ship it.
2. Split `gui.py` into `gui/pages/*.py` + a view-model layer.
3. **Snapshot-then-act**: btrfs/timeshift snapshot before destructive batches, with "Undo last action". This is the feature that makes a system tool trustworthy enough to recommend.
4. Flathub submission (`flatpak` topic is already on the repo — finish the job) and AUR package.
5. Boot-time analysis page (systemd-analyze blame, with "safe to disable" annotations).
6. i18n (`gettext`) — Bangla + Spanish + German would show up in Flathub.
7. Export a "machine report" (PDF/JSON) — IT support shops will use this and mention you.
8. KDE/Wayland parity, ARM64 build.

---

## 6. The three you should **not** sell yet — and why

### easyui — rename first, it's a legal dead end
- **`easyui` on npm is deprecated and squatted by npm itself**, and "EasyUI" is a well-known 2010s jQuery UI framework (jeasyui). Publishing under this name is impossible today and a trademark fight tomorrow.
- `@easyui/react` is **not published** — nobody can install your library.
- `docs/PLAN.md` still says *"Nothing is built yet"* while 36 components and 38 test files exist. Any evaluator reads that first and leaves.
- **What to do:** rename (e.g. `@grithq/ui`, `@adeel/ui`, `nordwood`), publish to npm, build a docs site (Storybook or your playground), add visual regression tests, then monetise as **open-core**: free MIT core + paid Pro blocks/templates/Figma kit ($79–149 lifetime, Lemon Squeezy/Polar). Component libraries are a *long* trust game — treat it as brand-building, not revenue, for 12 months.
- Genuine strength: the token → CSS-variable → runtime theming pipeline is a real differentiator. That's what shadcn users complain about.

### pinflow — good engineering, wrong legal footing
- Real system: scheduler, calendar, queue, analytics, AI vision metadata via OpenRouter, Next.js UI with tests.
- **Risk:** automating posting to Pinterest with a personal access token almost certainly violates Pinterest's Terms and gets your customers' accounts banned. Selling that is a refund-and-chargeback factory.
- **Fix before selling:** move to the official Pinterest API v5 with an approved app, publish rate limits visibly, never touch scraping. Then reposition from "Pinterest bot" to **"AI content repurposing for small commerce"** (one product photo → pin, story, caption, alt-text, scheduled across Pinterest/Instagram/Facebook).
- Buyer: Etsy/POD/Shopify sellers, Bangladeshi handicraft and fashion exporters (ties into §4 nicely — same customer, different budget).
- Price: $9–29/mo. But this is month 4+ work, not month 1.

### metro-optics — a service, not a product
- Clean React 19 + Firebase storefront with prescription management and admin. Firebase-only means no real payments and no inventory server.
- **Sell it as a fixed-price build**: ৳45,000–90,000 for a local eyewear/pharmacy/grocery retailer. Or as a template on Gumroad/ThemeForest ($39–59) after adding Stripe + a backend. Its README's "Future Improvements" list is literally your sales pitch — rewrite it as a feature list, in a professional voice, not a college-project voice.

### ToyTopia — archive it
The README is written in a self-deprecating junior voice ("sorry if it looks a bit messy", "safely ignore console warnings hehe"). It is the first thing a client sees when they browse your repos. Either rewrite it professionally as a learning-project case study with what you'd do differently, or **archive the repo**. You have enough real work now that this costs more than it earns.

---

## 7. Portfolio hygiene — the 2-day job that unlocks everything

Do this before you talk to a single client. It is the highest ROI work on this list.

| # | Fix | Applies to | How |
|---|---|---|---|
| 1 | **Add descriptions** | 11 of 12 repos | `gh repo edit --description "..."` |
| 2 | **Add a licence** | 11 of 12 (only Preen has MIT) | For products you sell: dual licence (AGPL/commercial) or "All rights reserved + commercial licence available". For tools: MIT. **No licence = no buyer**, legally. |
| 3 | **Add topics** | 11 of 12 | e.g. Arbor: `code-analysis`, `architecture`, `developer-tools`, `nextjs`, `trpc`, `codebase-visualization` |
| 4 | **Add CI** | 11 of 12 (`etuitionhub-frontend` already runs 3 workflows — reuse it as the template) | GitHub Actions: typecheck + lint + test + build, badge in README |
| 5 | **Tag a release** | 11 of 12 | `v0.1.0` with changelog + screenshots. Releases signal "finished". |
| 6 | **Screenshots/GIF at the top** | Arbor ✓, etuition ✗, iehub ✗ | 3 images minimum: hero, key screen, admin. Record with Screen Studio / Kap. |
| 7 | **Reveal the backend** | e-TuitionBD | Publish `etuitionhub-backend` or publish an OpenAPI contract. Non-negotiable. |
| 8 | **Rewrite weak READMEs** | iehub-server (empty), ToyTopia, metro-optics, easyui (stale PLAN) | Problem → solution → screenshots → quick start → architecture → licence. |
| 9 | **Pin 6 repos** | profile | Arbor, e-TuitionBD, Import Export Hub, Preen, pinflow, easyui |
| 10 | **Update profile README** | mdadeel | It features only 2 projects and reads like a résumé. Add: who you help, 4 projects with one-line outcomes, "Hire me for X", response time, and a link to a paid-services page. Drop the "philosophy" section; buyers skim. |

---

## 8. Pricing, packaging and getting paid from Bangladesh

Realistic bands (convert at ~৳122/USD; adjust to the client, not the table):

| Offer | Price | Cadence | Effort per unit |
|---|---|---|---|
| Repo due-diligence audit (Arbor-powered PDF + call) | $299–$999 | per report | 4–8 h |
| Codebase health retainer (2 audits/mo + PR checks) | $299/mo | monthly | 8–12 h |
| Arbor Teams (SaaS, after billing + CI) | $49–149/team/mo | monthly | — |
| Coaching-centre portal (white-label e-Tuition) | ৳60k–150k + ৳5–12k/mo | setup + retainer | 3–6 weeks |
| Export house portal (iehub pilot) | ৳150k–250k | one-time | 3–6 weeks |
| Export house full platform | ৳400k–800k + ৳15–40k/mo | project | 2–4 months |
| Retail storefront build (metro-optics based) | ৳45k–90k | one-time | 1–2 weeks |
| Linux desktop utility build + packaging (Preen as proof) | ৳80k–250k | one-time | 2–4 weeks |
| Storefront/LP templates (Gumroad) | $29–59 | passive | 1 week each |

**Getting paid — the practical part**
- **Stripe does not support merchants in Bangladesh.** Use a **merchant-of-record**: Paddle, Lemon Squeezy or Polar.sh. They handle global card payments, VAT and chargebacks, and pay you out via Payoneer/Wise. This is the single most important unblocker for selling Arbor/Preen/templates internationally.
- **Local clients:** bKash/Nagad merchant + bank transfer, with a written scope + 40–50% advance + milestone invoices. Never start retail work without an advance.
- **Invoices:** a proper PDF invoice with a scope table and a change-request rate (e.g. ৳3,000/h) prevents 90% of scope creep.
- **Tax/VAT:** for B2B software services in BD, keep a VAT registration path in mind as you cross thresholds; talk to a local accountant before your first ৳5 lakh contract — it also makes you look like a company rather than a freelancer, which raises prices.

**Channels that fit you**
1. **Local, face-to-face** (highest conversion, lowest competition): Chattogram Chamber of Commerce, Agrabad C&F agent offices, EPZ enterprises, coaching centres around Nasirabad/GEC, optics/pharmacy retailers on CDA Avenue. One afternoon of walk-ins beats a week of cold email.
2. **Upwork/Fiverr productized gigs:** "I will audit your GitHub repo's architecture and give you a prioritised report" — this is a real category and your Arbor output is the portfolio piece.
3. **LinkedIn** (you have a profile): post one architecture map + one finding per week. Dev-tool audiences convert on visuals, and you have them.
4. **GitHub Marketplace** for Arbor once PR checks are live; **Flathub** for Preen (free distribution, real users).
5. **Facebook groups**: tutors/coaching-centre owner groups (BD, very active) and import-export/C&F groups. Where your B2B buyers literally already hang out.

---

## 9. 90-day plan

**Weeks 1–2 — Make the account credible**
Descriptions, topics, licences, CI on Arbor + Preen + e-TuitionBD, release tags, screenshots, pin 6 repos, rewrite profile README, publish or contract-document the e-TuitionBD backend, remove demo credentials from prod paths.

**Weeks 3–4 — Cash first: audits**
Finish Arbor PDF export via Playwright on the share page. Write 3 sample audit reports (audit 3 public open-source repos). Launch the gig on Upwork + a section on arborgit.vercel.app + one LinkedIn post. Target: **1–2 paid audits ($299–$999)**.

**Weeks 5–8 — The big ticket: iehub pilot**
Pick one Chattogram export house or C&F agent. Offer a free 3-month pilot in exchange for logo + testimonial. Ship the P0 feature set: documents, LC module, checklist, notifications, real README, seed script. In parallel, book 5 discovery calls with coaching centres using the e-Tuition demo.

**Weeks 9–12 — Turn one into a subscription**
Whichever of Arbor / iehub / e-Tuition closed, convert it to a retainer with a written SLA. Then wire billing (Paddle/Polar) for Arbor Teams so growth isn't purely your hours.

**What success looks like at day 90:** 3–4 case studies with real names, one retainer worth ৳15–40k/mo, 2 audit sales, Arbor with green CI + a release + billing, and 2 repos that a stranger can run in under 10 minutes.

---

## 10. The five sentences that matter

1. **Arbor is your product** — sell audits this month, subscriptions next quarter, marketplace listing after that.
2. **e-TuitionBD and Import Export Hub are white-label software**, not marketplaces. Sell them to institutions and export houses, never to consumers.
3. **Preen is proof of craft**, not a revenue line — use it to sell Linux desktop build work and to keep sponsorship flowing.
4. **easyui and pinflow cost you more than they earn right now**; rename the first, re-license the second, and don't put either on a sales page this quarter.
5. **Your code is already good enough to sell. Your packaging is not.** Two weeks of descriptions, licences, CI, releases and screenshots will do more for your income than two months of new features.


---

## Addendum (28 Oct 2026) — two corrections after deeper inspection

1. **CI is not 0/12; it is 1/12.** `etuitionhub-frontend` already runs three workflows: `test.yml` (lint + unit tests + a Playwright e2e against the live URL), `deploy.yml` (prebuilt Vercel deploy) and `react-doctor.yml` (PR health check). That changes it from "gap" to "template" — and it means the repo you were least sure about is the best-engineered operationally.

2. **e-TuitionBD's backend is a much larger product than §3 assumed.** Walking every request the frontend makes (370 call sites) shows the platform already implements: organisations with branches, courses, batches, enrollments, guardians, attendance summaries, exams and results publishing, staff roles and salaries, invoices, per-tenant subscription plans, tutor wallet with withdrawal approvals, an assignment lifecycle (submit/grade/return), a full AI teaching suite (lesson plans, curriculum mapping, assignment drafting, quiz generation and marking, study notes, streaming tutor chat, usage metering, feedback), moderation reports, admin impersonation with audit, and platform reporting.

   That repositions the offer in §3. Do not lead with "tuition marketplace" — lead with **institute management system for coaching centres and schools**, with the marketplace as the student-acquisition hook. Buyers are principals and centre owners, the deal is ৳150,000–400,000 plus a monthly retainer, and the modules they ask about (attendance, results, fees, guardians, staff) already exist. The marketplace is what makes it distinctive, not what you open with.
