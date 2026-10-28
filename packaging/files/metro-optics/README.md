# Metro Optics

**A complete eyewear storefront with prescription handling, live inventory and an admin back office.** Built for a single-location optical retailer that wants to sell online without handing a monthly fee to a SaaS platform.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)](https://vite.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Firebase](https://img.shields.io/badge/Firebase-FFCA28?logo=firebase&logoColor=black)](https://firebase.google.com/)

> **Live:** [metro-optics.vercel.app](https://metro-optics.vercel.app)

<!-- SCREENSHOT: replace with 2–3 real screenshots (shop grid, product detail, admin). -->

---

## Features

**Storefront**
- Home with featured collections and category browsing
- Shop with filtering, sorting and search over the frame catalogue
- Product detail with image gallery, lens options, frame specifications and availability
- **Compare** up to several frames side by side
- Cart and checkout
- **Order tracking** by order reference, plus a printable **invoice** on order confirmation
- Profile area: saved addresses, wishlist, order history
- About, Contact, FAQ pages

**Prescriptions**
- Upload and store a prescription with each order
- Prescription details captured per line item so an order can be fulfilled against the right lens specification

**Admin back office**
- Product, category and inventory management
- Order management with status transitions
- Customer overview
- **Seeder page** to populate a new store with demo catalogue data

**Platform**
- Firebase Authentication (email/password + Google), with role-based access for the admin area
- Light and dark themes
- Fully responsive, with Radix primitives for accessible menus, dialogs, tabs and selects

## Tech stack

React 19 · Vite · React Router 7 · Tailwind CSS · Radix UI · Phosphor Icons · Firebase Auth + Firestore + Storage · react-hook-form + Zod · Recharts · Sonner

## Getting started

```bash
git clone https://github.com/mdadeel/metro-optics.git
cd metro-optics
npm install
cp .env.example .env      # add your Firebase project config
npm run dev               # http://localhost:5173
```

### Environment

Create a Firebase project, enable **Authentication** (email/password + Google), **Firestore** and **Storage**, then add:

```env
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
VITE_FIREBASE_PROJECT_ID=
VITE_FIREBASE_STORAGE_BUCKET=
VITE_FIREBASE_MESSAGING_SENDER_ID=
VITE_FIREBASE_APP_ID=
VITE_FIREBASE_MEASUREMENT_ID=
VITE_APP_URL=http://localhost:5173
VITE_BKASH_NUMBER=
```

After the first run, sign in as an admin and open the **Seeder** page to create catalogue data.

> ⚠️ `VITE_FIREBASE_*` values are **Firebase web config, not secrets** — they are meant to be public. Your real security boundary is **Firestore security rules**; make sure those are written and published before going live. Firebase client config alone does not protect your data.

## Architecture

```
src/
├── pages/          public shop, checkout, profile, admin
├── layouts/        StoreLayout, AdminLayout, ProfileLayout
├── components/     catalogue, cart, forms, charts, UI primitives
├── context/        auth + cart + theme providers
├── hooks/          Firestore subscriptions and form hooks
├── lib/            Firebase bootstrap, validators, formatters
└── data/           seed catalogue
```

Data access is client-side through the Firebase SDK. That makes deployment trivial (a static host) and keeps running costs near zero, at the cost of doing authorisation in security rules rather than in a server — which is exactly why the rules matter.

## Status

This is a **complete, deployable storefront template**, and being precise about what's missing:

- ✅ All storefront, account and admin flows are implemented against Firestore.
- ✅ Prescription capture, compare, invoices and order tracking work.
- ⚠️ **Checkout is cash-on-delivery / bKash details only** — there is no payment gateway integration and no automated payment confirmation.
- ⚠️ Inventory decrements are client-driven; a Cloud Function or server route should own them before high-volume use.
- ⚠️ No automated tests yet.
- ⚠️ Firestore security rules are project-specific and must be authored per deployment.

## Roadmap

- [ ] Payment gateway (bKash/Nagad merchant API, or SSLCommerz) with server-side confirmation
- [ ] Cloud Functions for inventory decrement, order emails and stock alerts
- [ ] Prescription verification workflow for the admin (approve / reject / request re-upload)
- [ ] Virtual try-on (face-landmark overlay) — genuinely useful for eyewear, not a gimmick
- [ ] Bangla language support
- [ ] Loyalty and referral codes

## Licence

[MIT](./LICENSE) © Shahnawas Adeel — use it, modify it, deploy it for your own store. Attribution appreciated, not required.

Need it customised, branded and deployed with a payment gateway? That's available as a fixed-scope engagement: [shahnawasadeel@gmail.com](mailto:shahnawasadeel@gmail.com).
