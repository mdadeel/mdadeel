# Import Export Hub — API

**Backend for a B2B import/export platform.** Multi-organisation tenancy, role-based permissions, RFQ workflows, document handling, disputes, webhooks and a full audit trail — built for export houses, buying houses and C&F agents.

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](./LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-339933?logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![Express](https://img.shields.io/badge/Express-4-000000?logo=express&logoColor=white)](https://expressjs.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/atlas)
[![Firebase Auth](https://img.shields.io/badge/Firebase_Auth-FFCA28?logo=firebase&logoColor=black)](https://firebase.google.com/docs/auth)

> Client application: [mdadeel/iehub-client](https://github.com/mdadeel/iehub-client) · Live: [iehub.vercel.app](https://iehub.vercel.app)

---

## What it does

An export business runs on four things: **who it sells to**, **what the terms are**, **which documents exist**, and **who is allowed to touch them**. This API models all four.

- **Organisations as tenants.** Every record belongs to an organisation. Membership is explicit (`OrganizationMember`), invitations are token-based (`Invite`), and a resolver puts the caller's organisation on every request.
- **Granular permissions.** Three separate role dimensions — platform roles (`Super Admin`, `Operations Admin`, `Compliance Admin`, `Finance Admin`, `Support Admin`), organisation roles (`Owner` → `Viewer`) and additive trade roles (`ProcurementManager`, `ProcurementAgent`, …) — combined into permission keys checked by a single `requirePermission` middleware on writer endpoints.
- **RFQ to purchase order.** Buyers raise a request for quotation; the seller counters, the buyer accepts, and the RFQ converts to an order in one call.
- **Documents.** Presigned upload URLs, confirmation, per-import document checklists, and a document list scoped to the caller's organisation.
- **Imports and delivery.** Import lifecycle with status transitions, delivery confirmation, and document attachment.
- **Disputes.** Raise, respond, resolve — with the counterparty and admin both able to act.
- **Webhooks.** Subscriptions with test delivery, so a client's ERP can be notified when an RFQ or dispute changes.
- **Audit log.** An append-only record written on privileged actions, with a platform-admin read endpoint.
- **Analytics and SEO.** Exportable analytics, plus `sitemap.xml` generation for the public catalogue.

## API surface

All routes are mounted under `/api`.

| Mount | Routes |
|---|---|
| `/api/products` | `GET /` · `GET /:id` · `POST /` · `PATCH /:id` · `PATCH /:id/verify` · `DELETE /:id` |
| `/api/rfq` | `GET /` · `POST /` · `PATCH /:id/counter` · `PATCH /:id/accept` · `POST /:id/convert` · `POST /:id/convert-to-po` |
| `/api/imports` | `GET /:email` · `POST /` · `PATCH /:id/status` · `PATCH /:id/confirm-delivery` · `GET /:id/documents` · `PATCH /:id/attach-document` |
| `/api/documents` | `GET /` · `GET /:id` · `POST /presigned-upload` · `POST /:id/confirm-upload` |
| `/api/disputes` | `GET /` · `POST /` · `GET /:id` · `PATCH /:id/respond` · `PATCH /:id/resolve` |
| `/api/organizations` | `POST /` · `GET /mine` · `GET /:id` · `PATCH /:id` · `GET /invites/mine` · `POST /invites/:token/accept` |
| `/api/company` | `GET /:email` · `POST /` |
| `/api/webhooks` | `GET /` · `POST /` · `PATCH /:id` · `DELETE /:id` · `POST /:id/test` |
| `/api/admin` | `GET /metrics` · `GET /orders` · `GET /entities` · `PATCH /entities/:email/kyb` · `GET /audit-logs` |
| `/api/analytics` | `GET /export` |
| `/api/seo` | `GET /sitemap.xml` |
| `/api/config` | `GET /` — public client config (Firebase web keys, feature flags) |
| `/api/health` | `GET` — liveness + dependency status |

## Data model

`Organization` · `OrganizationMember` · `Invite` · `CompanyProfile` · `Product` · `RFQ` · `Import` · `Document` · `Dispute` · `AuditLog` · `WebhookSubscription`

Mongoose models live in [`models/`](./models).

## Quick start

**Prerequisites:** Node.js 18+, a MongoDB database (Atlas or local), a Firebase project.

```bash
git clone https://github.com/mdadeel/iehub-server.git
cd iehub-server
npm install
cp .env.example .env      # fill in the values below
npm run dev               # http://localhost:5000, GET / returns a service banner
```

Verify it is up:

```bash
curl http://localhost:5000/api/health
```

### Environment

| Variable | Required | Purpose |
|---|---|---|
| `PORT` | no | Default `5000` |
| `NODE_ENV` | no | `development` / `production` |
| `LOG_LEVEL` | no | `debug` / `info` / `warn` / `error` |
| `MONGODB_URI` | **yes** | MongoDB connection string |
| `CLIENT_URL` | **yes** | Allowed CORS origin(s), comma-separated |
| `ADMIN_EMAILS` | **yes** | Comma-separated platform administrators |
| `FIREBASE_API_KEY` … `FIREBASE_MEASUREMENT_ID` | **yes** | Firebase **web** config, served to the client via `GET /api/config` |
| `FIREBASE_SERVICE_ACCOUNT` | recommended | Admin SDK service account (raw JSON or base64) for token verification |
| `FIREBASE_CLIENT_EMAIL`, `FIREBASE_PRIVATE_KEY` | alternative to the above | Split service-account credentials |
| `ENABLE_DEV_SANDBOX` | no | Development-only synthetic tokens. **Never enable in production.** |

Environment is validated at boot by [`config/validateEnv.js`](./config/validateEnv.js): the process refuses to start with a missing or malformed configuration rather than failing later at request time.

## Architecture

```
index.js                 app wiring: correlation ID → CORS → JSON → rate limit → routes → error handler
config/validateEnv.js    fail-fast environment validation
lib/firebaseAdmin.js     Admin SDK init (JSON or split credentials)
lib/roles.js             platform / organisation / trade roles → permission keys
middleware/
  correlationId.js       request ID propagated into logs and error responses
  authMiddleware.js      Firebase ID token → req.user
  resolveOrg.js          caller's organisation attached to the request
  requirePermission.js   permission gate for writer endpoints
  rateLimiter.js         global + per-route limits
models/                  Mongoose schemas
routes/                  one router per resource
```

**Error handling:** a single global error handler returns a consistent JSON shape with a correlation ID, so a client error report can be traced to a log line.

**Security posture:** Firebase ID tokens verified server-side, secrets never sent to the client, CORS restricted to explicit origins, Firebase *web* config served deliberately through `/api/config`, `ENABLE_DEV_SANDBOX` guarded against production use.

## Status

This is a working API with a live client, and it is honest about its gaps:

- ✅ All resource routes above are implemented and wired to MongoDB.
- ✅ Environment validation, correlation IDs, rate limiting and RBAC middleware are in place.
- ⚠️ **No automated tests yet.** The permission middleware is the highest-risk untested surface; adding tests there is the top priority.
- ⚠️ Document storage currently includes a mock upload/download pair alongside presigned URLs; a real object-store backend (S3/R2) is required for production.
- ⚠️ No OpenAPI specification is published yet.
- ⛔ No payment, invoicing or Letter-of-Credit modules yet — see the roadmap.

## Roadmap

Prioritised by what export houses actually ask for first:

- [ ] Tests for auth + permission middleware, then route-level integration tests
- [ ] OpenAPI 3 spec + Postman collection + seed script
- [ ] Commercial invoice, packing list and proforma invoice generation
- [ ] Letter of Credit module: terms, amendments, expiry alerts
- [ ] Per-shipment document checklist with requirements by destination and Incoterm
- [ ] HS code lookup with assisted classification
- [ ] Incoterms 2020 calculator and landed-cost estimator in BDT
- [ ] Buyer/supplier verification (trade licence, TIN/BIN, bank reference)
- [ ] Shipment tracking with a public buyer-facing status page
- [ ] Bulk CSV/Excel import for products and buyer lists

## Licence

**Proprietary — all rights reserved.** Public for review only; production use, redistribution or white-label deployment requires a written commercial licence: [shahnawasadeel@gmail.com](mailto:shahnawasadeel@gmail.com). See [`LICENSE`](./LICENSE).

---

Built by [Shahnawas Adeel](https://mdadeel.me) · Chattogram, Bangladesh
