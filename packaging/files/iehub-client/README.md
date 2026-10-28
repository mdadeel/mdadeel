# Import Export Hub — Client

**A trade platform for export businesses.** Verified organisations, a product catalogue, quotation workflows, document vaults, disputes and a logistics view — in one workspace instead of an inbox and a spreadsheet.

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](./LICENSE)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-7-646CFF?logo=vite&logoColor=white)](https://vite.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-38B2AC?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Firebase](https://img.shields.io/badge/Firebase_Auth-FFCA28?logo=firebase&logoColor=black)](https://firebase.google.com/docs/auth)

> **Live:** [iehub.vercel.app](https://iehub.vercel.app) · **API:** [mdadeel/iehub-server](https://github.com/mdadeel/iehub-server)

<!-- SCREENSHOT: replace with 3 real screenshots (landing, product catalogue, organisation dashboard). -->

---

## What it does

| Area | Detail |
|---|---|
| **Organisations** | Create an organisation, invite colleagues by token link, manage members and roles, and operate entirely inside the organisation's data boundary |
| **Catalogue** | Browse and filter global products by category, price and rating; product detail with seller and origin information |
| **Exports** | Full CRUD over your own export listings, with status tracking |
| **Imports** | One-click import of a product into "My Imports", with quantity validation and inventory decrement |
| **RFQs** | Raise a quotation request, receive counters, accept, and convert to an order |
| **Documents** | A document vault per organisation and per shipment, with upload state tracking |
| **Disputes** | Open a dispute against a counterparty, respond, and track resolution |
| **Logistics** | Shipment and delivery views |
| **Admin** | Platform metrics, entity list, KYB (know-your-business) review, audit log |
| **Insights** | Market insight and trade-expert pages, with charts via Recharts |

## Tech stack

React 19 (Vite) · React Router 7 · Tailwind CSS 4 · Radix UI · Lucide icons · Framer Motion · Recharts · Firebase Auth (email/password + Google) · TanStack Query · Zod · react-hot-toast

## Getting started

```bash
git clone https://github.com/mdadeel/iehub-client.git
cd iehub-client
npm install
npm run dev            # http://localhost:5173
```

The client needs the [API](https://github.com/mdadeel/iehub-server) running, and it stores **no secrets**. Firebase *web* configuration is fetched from the backend at `GET /api/config` (see [`src/utils/firebase.config.js`](./src/utils/firebase.config.js)), so there is no `VITE_*` env file to fill in — point the client at your API and it configures itself. That also means only server-side environment changes are needed to move between staging and production.

```bash
npm run build          # production bundle
npm run preview
npm run lint
```

### Seeded accounts

The hosted demo exposes seeded users for review. Demo credentials are for the demo tenant only.

## Architecture

```
src/
├── pages/         22 route-level screens (marketplace, organisation, admin)
├── layouts/       public, dashboard and admin shells
├── components/    catalogue, RFQ, document, chart and form components
├── context/       auth + organisation providers
├── lib/           permission helpers, category taxonomy, utilities
├── hooks/         data fetching and form hooks
└── utils/         Firebase bootstrap from backend config
```

**Authorisation is enforced server-side.** The client's `lib/permissions.js` mirrors the server's role → permission map so the UI can hide what a user can't do, but every writer endpoint is independently gated by `requirePermission` on the API. Treat the client checks as ergonomics, not security.

## Status

- ✅ All screens above are implemented and connected to the live API.
- ✅ Authentication, organisation onboarding and invitation acceptance work end to end.
- ⚠️ Test coverage is minimal; the client has no component or E2E suite yet.
- ⚠️ Document uploads depend on the API's presigned-URL flow, which is not yet backed by a production object store.
- ⛔ Payments, invoicing and Letter of Credit handling are not implemented — they are the next product milestone.

## Licence

**Proprietary — all rights reserved.** Public for review only. Commercial, white-label and custom deployments are available under a written licence: [shahnawasadeel@gmail.com](mailto:shahnawasadeel@gmail.com). See [`LICENSE`](./LICENSE).

---

Built by [Shahnawas Adeel](https://mdadeel.me) · Chattogram, Bangladesh
