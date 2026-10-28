# e-TuitionBD — API & Platform

**Backend for a multi-tenant EdTech platform.** Tutoring marketplace, organisation (coaching centre / school) management with branches, batches, attendance and exams, subscription plans, wallet and payouts, and an AI teaching assistant.

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](./LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-Express-339933?logo=nodedotjs&logoColor=white)](https://expressjs.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Firebase Auth](https://img.shields.io/badge/Firebase_Auth-FFCA28?logo=firebase&logoColor=black)](https://firebase.google.com/docs/auth)

> **Client:** [mdadeel/etuitionhub-frontend](https://github.com/mdadeel/etuitionhub-frontend) · **Live:** [e-tuitionhub.vercel.app](https://e-tuitionhub.vercel.app)

---

> **Note on this README.** This document was written from the client's API contract and the code that calls this service — the endpoint inventory below is real, extracted from every request the frontend makes. Sections marked **TODO (owner)** need details that can only be read from this repository (runtime scripts, exact env names, deployment topology). Fill those in before sharing the repo with anyone.

## What this service does

It is not only a tuition marketplace. There are two products in one API:

1. **A marketplace** — students post requirements, tutors apply, both sides hire, pay and run sessions.
2. **A multi-tenant institution platform** — a coaching centre or school gets an organisation with branches, courses, batches, enrollments, attendance, exams, results publishing, staff roles, salaries, invoices and its own analytics. Tenants are isolated by organisation ID, and access is governed by per-organisation roles.

Billing is subscription-based at the organisation level, plus a tutor wallet with withdrawal approvals.

## API surface

All routes are served under `/api` (with the organisation platform under `/api/v1`).

### Authentication and session

| Route | Purpose |
|---|---|
| `POST /api/auth/jwt` | Exchange a Firebase ID token for the platform session |
| `POST /api/auth/refresh` | Rotate the session (the client queues and retries failed requests during rotation) |
| `POST /api/auth/logout` | End the session and clear cookies |

Sessions are cookie-based (`httpOnly`), with a `csrf-token` cookie the client echoes on unsafe methods. The client holds no tokens in `localStorage`.

### Marketplace

| Group | Routes |
|---|---|
| Tutors | `GET /api/tutors` (filter, sort, paginate) · `GET /api/tutors/:id` · `GET /api/tutors/:id/reviews` · `GET /api/tutors/:id/availability` · `POST /api/tutors/heartbeat` |
| Tuitions | `GET /api/tuitions` · `GET /api/tuitions/:id` · `PATCH /api/tuitions/:id/status` · `GET /api/tuitions/similar/:id` |
| Applications | `GET/POST /api/applications` · `GET /api/applications/:id` · `GET /api/applications/student/:id` · `GET /api/applications/tutor/:id` |
| Connections (hiring) | `GET/POST /api/connections` · `POST /api/connections/:id/confirm` · `.../respond` · `.../pause` · `.../complete` · `.../cancel` · `.../propose-details` · `.../mark-free-trial` · `.../mark-paid` · `.../privacy` |
| Hire requests | `GET/POST /api/hire-requests` · `POST /api/hire-requests/:id/accept` · `.../decline` · `.../counter` |
| Sessions | `GET /api/sessions` · `POST /api/sessions/:id/confirm` · `POST /api/sessions/:id/dispute` · `GET /api/sessions/stats/summary` |
| Bookings | `GET /api/bookings/:id` · `GET /api/bookings/student/:id` |
| Bookmarks | `GET/POST/DELETE /api/bookmarks`, `/api/bookmarks/tuitions` |
| Search | `GET /api/search/combined?q=` · `GET/POST /api/search-alerts` |

### Payments, wallet and payouts

| Route | Purpose |
|---|---|
| `POST /api/payments/manual` | Record a bKash/Nagad/Rocket/bank payment with proof |
| `GET /api/payments/all` · `/api/payments/student/:id` · `/api/payments/tutor/:id` | Ledger views per role |
| `POST /api/payments/:id/reject` | Admin rejection with reason |
| `GET /api/receipts/me` | Receipts for the caller |
| `GET /api/wallet/me` · `POST /api/wallet/withdraw` | Tutor wallet and withdrawal request |
| `POST /api/wallet/admin/withdrawals/:id/approve` · `.../reject` · `.../mark-paid` | Payout workflow |
| `GET /api/admin/finance/reconciliation` | Cross-check of manual payments, wallet and payouts |

### Organisation platform (`/api/v1`)

| Area | Routes |
|---|---|
| Organisations | `GET/POST /api/v1/organizations` · `GET /api/v1/organizations/my/orgs` · `GET /api/v1/organizations/slug/:slug` · `PATCH /api/v1/organizations/:id` · `POST .../activate`, `.../suspend`, `.../ban`, `.../unban` · `POST .../notify` |
| Membership | `GET/POST .../members` · `PATCH/DELETE .../members/:id` · `GET/POST .../invites` · `GET/POST .../join-requests` · `POST .../join-requests/:id` · `POST .../leave` |
| Roles | `GET/POST .../roles` · `PATCH/DELETE .../roles/:id` |
| Branches | `GET/POST .../branches` · `PATCH .../branches/:id` |
| Academics | `.../courses` · `.../batches` · `.../subjects-list` · `.../schedules` · `.../sessions` |
| People | `.../students` (+ `import` / `export` CSV) · `.../guardians` · `.../tutors` · `GET .../tutors/:id/workload` |
| Attendance | `GET .../attendance/summary` · `GET .../attendance/low` |
| Exams and results | `.../exams` · `GET .../results/exams/:id` · `POST .../results/exams/:id/publish` |
| Money | `.../invoices` · `.../payments` · `POST .../salaries/:id/approve` |
| Analytics | `GET .../analytics/dashboard` · `GET .../analytics/branches` |
| Moderation | `GET /api/v1/moderation` · `GET /api/v1/moderation/reports` |

### Subscriptions and plans

`GET /api/v1/plans` · `GET /api/v1/plans/public` · `GET/POST /api/v1/plans/:id` · `GET /api/v1/subscriptions` · `POST /api/v1/subscriptions/:id/subscription/cancel`

### Assignments and AI teaching tools

| Route | Purpose |
|---|---|
| `GET/POST /api/assignments` · `POST .../:id/submit` · `.../:id/grade` · `.../:id/return` | Assignment lifecycle with submission, grading and return |
| `POST /api/ai/tutor/lesson-plan` | Generate a lesson plan |
| `POST /api/ai/tutor/curriculum` | Curriculum mapping |
| `POST /api/ai/tutor/assignment` | Assignment drafting |
| `POST /api/ai/quiz/generate` · `POST /api/ai/quiz/submit` · `GET /api/ai/quiz/history` | Question generation and auto-marking |
| `GET/POST /api/ai/notes` · `PATCH/DELETE /api/ai/notes/:id` | Study notes |
| `POST /api/ai/chat` · `POST /api/ai/chat/stream` | Tutor chat, including a streaming endpoint |
| `GET /api/ai/usage` · `GET/PATCH /api/ai/settings` | Quotas and provider configuration |
| `POST /api/ai/feedback` · `POST /api/ai/tutor-recommendation-click` | Quality signals |

### Platform administration

| Route | Purpose |
|---|---|
| `POST /api/admin/promote-to-admin/:id` · `.../demote-from-admin/:id` | Admin grants |
| `POST /api/admin/impersonate/:id` · `POST /api/admin/impersonate/exit` | Time-boxed support impersonation |
| `POST /api/admin/tutors/:id/approve` · `.../reject` · `.../request-resubmission` | Tutor verification workflow |
| `PATCH /api/admin/users/bulk` | Bulk user actions |
| `GET /api/admin/reports` · `POST /api/admin/reports/run` | Report definitions and execution |
| `GET /api/admin/circuit-breakers` | Upstream dependency health |
| `GET /api/audit-logs` · `GET /api/audit-logs/actions` | Append-only audit trail |
| `GET /api/analytics/platform-overview` · `/api/analytics/stats` · `/api/analytics/popular-searches` · `/api/analytics/zero-result-searches` | Platform analytics, including search quality |
| `GET /api/settings/public` · `GET/PATCH /api/settings` · `PATCH /api/settings/bulk` | Platform settings (public subset served separately) |
| `GET /api/v1/verifications/:id/ai-extract` | Document extraction for verification review |

### Content, uploads and mail

`GET /api/templates` · `GET /api/templates/public` · `GET /api/testimonials` · `GET /api/contact` · `POST /api/upload` · `POST /api/upload/payment-screenshot` · `GET /api/mails/:id` · `POST /api/mails/:id/read`

## Security model

- **Identity:** Firebase Authentication (email/password + Google). The API verifies Firebase ID tokens server-side and never trusts client-supplied identity.
- **Session:** short-lived cookie session with refresh rotation; `httpOnly` cookies, CSRF token echoed on unsafe methods. No tokens in browser storage.
- **Authorisation:** role checks at four levels — platform admin, organisation role (owner → viewer), trade/functional role, and resource ownership. Organisation-scoped routes verify membership before reading or writing tenant data.
- **Audit:** privileged actions (role changes, verification decisions, payouts, impersonation) are recorded in an append-only audit log.
- **Impersonation:** explicitly entered and exited, time-bounded, and audited.

> **TODO (owner):** confirm the exact token TTLs, cookie flags (`SameSite`, `Secure`), CSRF strategy, and whether refresh tokens rotate with reuse detection. These are the details a security reviewer will ask about first.

## Running it

> **TODO (owner):** replace this section with the real commands from this repository's `package.json` (`dev`, `start`, migrations/seeders), the exact `.env` variable names, and the Node version. The template below is the expected shape.

```bash
git clone https://github.com/mdadeel/etuitionhub--backend.git
cd etuitionhub--backend
npm install
cp .env.example .env      # MongoDB URI, Firebase Admin credentials, session secret, AI provider keys
npm run dev
```

> **TODO (owner):** list every environment variable here. At minimum a reader will need: MongoDB URI, Firebase Admin service account, session/cookie secret, allowed client origin, AI provider key, and object storage credentials.

## Deployment

The client pointed at this service has **no environment variables of its own** — it fetches public configuration from this API and hardcodes the production base URL. Consequences worth knowing:

- Rotating or renaming the deployment domain requires a client change (`src/config/api.js` in the frontend), not a config change.
- **Realtime chat needs a dedicated Socket.IO host in production.** The client resolves `SOCKET_URL` to `null` in production builds, so chat silently degrades to HTTP polling. Deploying a socket service (Railway/Fly.io) and pointing the client at it is the single highest-impact infrastructure fix on this platform.
- WebRTC session rooms need a **TURN server**; without one, calls fail behind carrier-grade NAT, which is the norm on mobile networks in Bangladesh.

> **TODO (owner):** document the actual deployment target (Vercel serverless? Node host?), the region, and how background jobs and sockets are scheduled there.

## Status

- ✅ The full API surface above is implemented and consumed by the live client.
- ✅ Organisation tenancy, subscription plans, wallet/payouts and the audit trail are in place.
- ⚠️ **No published OpenAPI specification** — the endpoint inventory in this README was reconstructed from the client. Generating OpenAPI from the router definitions is the highest-value documentation task here.
- ⚠️ No automated test suite is referenced by the client repository; the authorisation layer is the highest-risk area to leave untested.
- ⚠️ Payment handling is **manual-proof based** (screenshot + admin verification), not gateway-integrated. That is a deliberate design for bKash/Nagad in Bangladesh, but it means reconciliation is a human process.
- ⚠️ AI endpoints depend on an external provider; quota and cost controls live in `/api/ai/settings` and `/api/ai/usage` and should be reviewed per tenant.

## Roadmap

- [ ] OpenAPI 3 specification, generated from the routers, published here
- [ ] Automated tests: auth, tenancy isolation, and permission boundaries first
- [ ] Dedicated Socket.IO deployment so realtime chat works in production
- [ ] TURN server for WebRTC session rooms
- [ ] Gateway integration (bKash/Nagad merchant API) with server-side confirmation and idempotency, replacing manual proof review
- [ ] SMS notifications for guardians and batch reminders (local gateway: SSL Wireless / Robi)
- [ ] Attendance offline sync for low-connectivity classrooms
- [ ] Per-tenant data export (a real requirement for schools)

## Licence

**Proprietary — all rights reserved.** White-label deployments for coaching centres, schools and tutoring organisations are available under a written commercial licence: [shahnawasadeel@gmail.com](mailto:shahnawasadeel@gmail.com). See [`LICENSE`](./LICENSE).

---

Built by [Shahnawas Adeel](https://mdadeel.me)
