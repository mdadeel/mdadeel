#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# W1 — Repository metadata (description + topics)
#
# Settings only. No commits, no branches, no file changes. Fully reversible.
# Run as the account owner:  gh auth login   (must have admin on each repo)
#
# Usage:
#   ./metadata.sh            # apply everything
#   ./metadata.sh --dry-run  # print what would be sent, change nothing
#   ./metadata.sh Arbor      # apply to one repo only
# ---------------------------------------------------------------------------
set -uo pipefail

OWNER="mdadeel"
DRY_RUN=0
ONLY=""
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    -*) echo "unknown flag: $arg"; exit 2 ;;
    *) ONLY="$arg" ;;
  esac
done

FAILED=0
SKIPPED=0
CHANGED=0

apply() {
  local repo="$1" desc="$2" topics="$3"

  if [ -n "$ONLY" ] && [ "$repo" != "$ONLY" ]; then return; fi

  # Never write to a repo we cannot administer.
  local can_admin
  can_admin=$(gh api "repos/$OWNER/$repo" --jq '.permissions.admin' 2>/dev/null)
  if [ "$can_admin" != "true" ]; then
    printf '  SKIP  %-24s (no admin access, or repo not visible)\n' "$repo"
    SKIPPED=$((SKIPPED + 1))
    return
  fi

  if [ "$DRY_RUN" -eq 1 ]; then
    printf '\n=== %s ===\n  description: %s\n  topics:      %s\n' "$repo" "$desc" "$topics"
    return
  fi

  local desc_ok=1
  gh api -X PATCH "repos/$OWNER/$repo" -f description="$desc" --jq '.name' >/dev/null 2>&1 \
    || desc_ok=0

  # Topics is a separate endpoint and must be sent as JSON.
  local topics_json
  topics_json=$(TOPICS="$topics" python3 -c '
import json, os
names = [t for t in os.environ["TOPICS"].split() if t][:20]   # GitHub caps at 20
print(json.dumps({"names": names}))
')
  local topics_ok=1
  printf '%s' "$topics_json" \
    | gh api -X PUT "repos/$OWNER/$repo/topics" --input - --jq '.names | length' >/dev/null 2>&1 \
    || topics_ok=0

  if [ "$desc_ok" -eq 1 ] && [ "$topics_ok" -eq 1 ]; then
    printf '  OK    %-24s description + %s topics\n' "$repo" "$(printf '%s' "$topics" | wc -w | tr -d ' ')"
    CHANGED=$((CHANGED + 1))
  else
    printf '  FAIL  %-24s (description:%s topics:%s)\n' "$repo" "$desc_ok" "$topics_ok"
    FAILED=$((FAILED + 1))
  fi
}

echo "Repo metadata — $OWNER$([ "$DRY_RUN" -eq 1 ] && echo '  [DRY RUN]')"

# --- Products you sell -------------------------------------------------------
apply Arbor \
 "Architecture and health audits for GitHub repositories: interactive dependency maps, prioritised findings, PR checks and shareable reports." \
 "code-analysis architecture developer-tools static-analysis codebase-visualization nextjs typescript trpc prisma software-quality"

apply etuitionhub-frontend \
 "Tuition marketplace and coaching-centre portal: role dashboards, realtime chat, WebRTC classrooms and bKash/Nagad checkout." \
 "edtech react vite marketplace bangladesh socket-io webrtc tailwindcss education saas"

apply etuitionhub--backend \
 "API and platform for a multi-tenant EdTech SaaS: marketplace, organisation management with branches, batches, attendance and exams, subscriptions and payouts." \
 "edtech nodejs express mongodb multi-tenant rbac rest-api saas education bangladesh ai"

apply iehub-client \
 "Client for a B2B import/export platform: verified organisations, product catalogue, RFQs, disputes and document tracking." \
 "b2b import-export trade react firebase logistics marketplace bangladesh"

apply iehub-server \
 "Express/MongoDB API for a B2B trade platform: multi-organisation tenancy, RBAC, RFQs, disputes, documents, webhooks and audit logs." \
 "nodejs express mongodb rbac rest-api b2b trade logistics webhooks audit-log"

# --- Credibility assets ------------------------------------------------------
apply Preen \
 "System setup, deep cleaning and tuning for Linux. GTK 3 app: install/remove apps, deep-clean with size preview, manage systemd services, simulate before you act." \
 "python zorin-os zorin-script appimage flatpak gtk3 linux system-cleaner system-optimizer systemd pygobject ubuntu"

apply pinflow \
 "AI-assisted Pinterest scheduling: vision-generated metadata, bulk CSV upload, calendar, queue and performance analytics." \
 "pinterest automation scheduling python fastapi nextjs content-marketing ai"

apply easyui \
 "Accessible React component library with runtime design-token theming — change accent, radius and font without touching component code." \
 "react ui-components design-system design-tokens accessibility typescript tailwindcss component-library"

apply metro-optics \
 "Eyewear storefront with prescription management, live inventory and an admin dashboard. React 19 + Firebase." \
 "ecommerce react firebase tailwindcss storefront prescriptions eyewear retail"

# --- Profile -----------------------------------------------------------------
apply mdadeel \
 "Profile README — full stack developer building Arbor, e-TuitionBD and Import Export Hub." \
 "profile-readme developer-portfolio full-stack typescript react nextjs bangladesh"

# Intentionally untouched:
#   ToyTopia                — user decision: skip until it is upgraded
#   CodeArena-TeamProject   — fork
#   Doctoria                — fork

echo
echo "---------------------------------------------"
echo "changed: $CHANGED   skipped: $SKIPPED   failed: $FAILED"
[ "$FAILED" -eq 0 ] || { echo "Some repos failed — check that your token has 'Administration' write access."; exit 1; }
echo
echo "Next: pin the 6 repos that match the sales story (see packaging/README.md §4)."
