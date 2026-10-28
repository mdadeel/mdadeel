# e-TuitionBD — Frontend

**A tuition marketplace and coaching-centre portal for Bangladesh.** Students post what they need, tutors apply, admins verify and settle payments — across Bangla, English, Cambridge and IB curricula.

[![Frontend Tests](https://github.com/mdadeel/etuitionhub-frontend/actions/workflows/test.yml/badge.svg)](https://github.com/mdadeel/etuitionhub-frontend/actions/workflows/test.yml)
[![Deploy](https://github.com/mdadeel/etuitionhub-frontend/actions/workflows/deploy.yml/badge.svg)](https://github.com/mdadeel/etuitionhub-frontend/actions/workflows/deploy.yml)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](./LICENSE)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-7-646CFF?logo=vite&logoColor=white)](https://vite.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3-38B2AC?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-4-010101?logo=socket.io&logoColor=white)](https://socket.io/)

<!-- SCREENSHOT: replace with 3 real screenshots (home, tutor search, tutor dashboard).
<p align="center"><img src="docs/screenshots/home.png" alt="Home page" width="85%"></p>
-->

> **Live demo:** [e-tuitionhub.vercel.app](https://e-tuitionhub.vercel.app) · **Backend:** separate, private repository (see [Architecture](#architecture))

---

## What it is

A three-sided platform built around one marketplace:

| Role | What they do |
|---|---|
| **Student / Guardian** | Post a tuition requirement, browse and filter verified tutors, book, pay, message, join the session room, track payments |
| **Tutor** | Build a verified profile, apply to tuitions, set availability and rates, run sessions, track earnings and withdrawals |
| **Institution** | Manage a branch with multiple tutors, batches and a shared inbox |
| **Admin** | Approval workflow, document verification, payment oversight, finance workspace, audit logs, platform analytics |

## Features

**Discovery**
- Tutor and tuition browsing with URL-synced filters (subject, class, area, language, price band), infinite scroll, saved searches
- Unified search with autocomplete, keyboard navigation and recent searches
- City landing pages and an organisation directory

**Hiring pipeline**
- Multi-step tutor application and tuition posting
- Tutor verification with document upload (NID, certificates) and admin review
- Live application tracking on both sides, with a public booking page for sharing

**Communication**
- Realtime 1:1 chat (Socket.IO) with read receipts, typing indicators and conversation previews
- Notifications with batch actions and realtime delivery
- **Session rooms** with WebRTC audio/video (`simple-peer`) plus in-call text chat

**Payments**
- Checkout with bKash, Nagad, Rocket and bank transfer
- Tutor earnings, withdrawal requests, and an admin finance workspace with approval and audit trail
- Parent guarantee (escrow-style hold) flow

**Platform**
- Role-aware dashboards behind a single shell
- Bangla/English i18n, PWA install support
- SEO: server-rendered meta for tutor/tuition/organisation pages, `sitemap.xml`, `robots.txt`, `llms.txt`
- Hardened response headers (HSTS, `X-Frame-Options`, `X-Content-Type-Options`, Permissions-Policy)

## Tech stack

React 19 · Vite 7 · React Router 7 · Tailwind CSS 3 · Radix UI · Framer Motion / `motion` · TanStack Query · Zustand · Socket.IO client · `simple-peer` (WebRTC) · Firebase Auth + Storage · Recharts · react-hook-form · i18next · `vite-plugin-pwa` · Vitest + Playwright

## Getting started

```bash
git clone https://github.com/mdadeel/etuitionhub-frontend.git
cd etuitionhub-frontend
npm install
npm run dev          # http://localhost:5173
```

This frontend needs the **e-TuitionBD backend running**. In development it calls `http://localhost:5000` (see [`src/config/api.js`](./src/config/api.js)); in production it calls the deployed backend.

The frontend deliberately holds **no secrets and no environment variables** — public configuration (Firebase web keys, feature flags, pricing) is served by the backend at `GET /api/config`. To point at a different backend, change the constant in `src/config/api.js`.

```bash
npm run build        # production bundle
npm test             # Vitest
npm run test:e2e     # Playwright
npm run lint
```

### Demo credentials

The hosted demo exposes seeded accounts for review. They are **read-only demo data**: never reuse those credentials for real work, and never publish your own tenant's credentials in a README.

## Architecture

```
src/
├── pages/            route-level screens (public, dashboard, admin)
├── components/       feature components (Dashboard/, Connections/, shared/)
├── services/         API client + sockets (axios instance with CSRF + refresh queue)
├── store/            Zustand stores
├── contexts/         auth, theme, socket providers
├── hooks/            data + UI hooks
├── locales/          en / bn translation bundles
└── config/           API URL resolution
```

**Backend:** a separate Express + MongoDB service, deployed independently and not public. Every `/api/*` request is proxied to it through `vercel.json`; tutor, tuition and organisation routes are rewritten to a server-side SEO renderer so social crawlers get real meta tags. If you need the API contract, ask — an OpenAPI description can be published without exposing the implementation.

**Realtime:** in development, Socket.IO runs inside the Express server. In production `SOCKET_URL` resolves to `null`, so the client falls back to HTTP polling/REST. A dedicated socket host (Railway/Fly.io) is the recommended next step for production chat.

**WebRTC:** peer-to-peer calls require a TURN server to work reliably behind carrier-grade NAT — which is the normal case on Bangladeshi mobile networks. Without TURN, expect some calls to fail to connect on 4G.

## Status

- ✅ Builds, lints and passes the frontend test suite in CI (`.github/workflows/test.yml`), including a Playwright smoke test against the deployed URL.
- ✅ Full marketplace flows are implemented end to end against the backend.
- ⚠️ Payment flows are integrated at the UI and API level; provider-side reconciliation (webhooks, refunds, settlement reports) is the outstanding work before real money moves at volume.
- ⚠️ Realtime chat degrades to polling in production until a dedicated socket host is deployed.
- ⚠️ Some admin screens read from seeded demo data (`src/data/mockData.js`) rather than live aggregates. Treat those views as design previews.
- ⛔ Not multi-tenant in the strict sense: one deployment serves one operator. White-label deployments are per-client.

## Licence

**Proprietary — all rights reserved.** This repository is public for review and portfolio purposes only. Reuse in another product, redistribution, or running it as a service requires a written commercial licence.

White-label deployment for coaching centres, schools and tutoring organisations is available: [shahnawasadeel@gmail.com](mailto:shahnawasadeel@gmail.com). See [`LICENSE`](./LICENSE).

---

Built by [Shahnawas Adeel](https://mdadeel.me)
