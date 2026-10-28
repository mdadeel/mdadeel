# easyui

**Accessible React components with runtime design-token theming.** Change the accent colour, corner radius and font on the fly — every component updates without a rebuild and without editing component code.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![React](https://img.shields.io/badge/React-18%2B-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![pnpm](https://img.shields.io/badge/pnpm-workspace-F69220?logo=pnpm&logoColor=white)](https://pnpm.io/)

> ⚠️ **Not yet published to npm.** `@easyui/react` is the internal package name and it is currently built from source. A rename and a public release are planned — `easyui` on npm is an unrelated, deprecated package, and "EasyUI" already refers to a different, established framework, so publishing under this name is not an option. See [Status](#status).

---

## Why another component library

Most component libraries make you choose: either the components are copied into your repo and you own them (great for control, painful to update), or they're a dependency and every visual choice is locked by a maintainer.

easyui takes a third path. **Design tokens are the single source of truth**, compiled to CSS custom properties, and exposed through a provider. That means:

- **Theming is runtime state, not a build step.** `<EasyUIProvider accent="#2563eb" radius="md">` restyles the whole tree — useful for white-label builds, per-tenant branding, and live theme switchers.
- **Tokens are layered.** Primitives (`blue-500`) feed semantic roles (`action-primary`), which feed component variables. Application code never references a raw primitive.
- **Accessibility is not a plugin.** Behaviour comes from headless primitives (Radix); keyboard interaction, focus management and ARIA wiring are inherited rather than re-implemented, and they're covered by automated a11y tests.

## Components

36 components, each with variants, sizes and states:

`accordion` · `alert` · `alert-dialog` · `aspect-ratio` · `avatar` · `badge` · `breadcrumb` · `button` · `card` · `choice` · `collapsible` · `combobox` · `dialog` · `dropdown-menu` · `empty` · `field` · `input` · `kbd` · `label` · `link` · `pagination` · `popover` · `progress` · `radio` · `select` · `separator` · `sheet` · `skeleton` · `slider` · `spinner` · `table` · `tabs` · `textarea` · `toast` · `toggle` · `tooltip`

Plus composed patterns: form fields with label/description/error wiring, empty states, and keyboard-hint affordances.

## Repository layout

```
packages/tokens      Design tokens (JSON) → CSS custom properties
packages/react       @easyui/react — components, provider, colour helpers, styles
apps/playground      Live theming playground (accent, radius, font, density)
docs/PLAN.md         Research, stack decisions and phased roadmap
```

## Usage

```tsx
import "@easyui/react/styles.css";
import { EasyUIProvider, Button } from "@easyui/react";

export function App() {
  return (
    <EasyUIProvider accent="#2563eb" radius="md">
      <Button>Get started</Button>
      <Button variant="secondary">Read docs</Button>
    </EasyUIProvider>
  );
}
```

Fonts are deliberately not bundled — load your own (the playground uses `@fontsource-variable/geist`) and pass `fontFamily` to `EasyUIProvider` to override the default.

Colour helpers handle the unglamorous part: given one accent, contrast-safe hover, active, disabled and focus states are derived automatically, so a custom brand colour doesn't produce unreadable buttons.

## Development

```bash
pnpm install
pnpm dev          # build the library, then start the playground
pnpm build        # tokens → library (ESM + CJS + types + CSS) → playground
pnpm test         # unit + accessibility tests
pnpm lint
pnpm typecheck
```

## Status

This is an actively developed library, pre-1.0 and pre-publication.

- ✅ 36 components implemented, all typed, all keyboard operable.
- ✅ Token pipeline builds end to end (JSON → CSS custom properties → component variables).
- ✅ 38 test files covering rendering, variants and accessibility assertions.
- ⚠️ **Not on npm yet** — installing it means building from source.
- ⚠️ No published documentation site; the playground is the current reference.
- ⚠️ No visual regression testing yet, which is the main risk for a component library.
- 🔜 Planned: rename to a publishable, non-conflicting package name; docs site; changesets + automated releases; dark-mode token parity; Figma token export.

`docs/PLAN.md` documents the original research and stack decisions. It was written before implementation and its early "nothing is built yet" framing is out of date — the component list above reflects what exists.

## Roadmap

- [ ] Rename + first public npm release with semantic versioning
- [ ] Documentation site with live examples and copy-paste snippets
- [ ] Visual regression tests (Playwright screenshots) in CI
- [ ] Dark mode token set with parity tests
- [ ] Data-heavy components: data table, date picker, command palette
- [ ] Figma library backed by the same token JSON

## Contributing

Issues and pull requests are welcome. Run `pnpm lint`, `pnpm typecheck` and `pnpm test` before opening a PR.

## Licence

[MIT](./LICENSE) © Shahnawas Adeel — free to use, modify and redistribute, including commercially.
