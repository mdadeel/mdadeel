#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Verify — re-runs the success criteria from REPO-PACKAGING-PLAN.md §2 and
# prints a table plus totals. Read-only: it changes nothing.
#
# Usage: ./verify.sh
# ---------------------------------------------------------------------------
set -uo pipefail
OWNER="${OWNER:-mdadeel}"

# One call for everything that lives on the repo object.
gh repo list "$OWNER" --limit 100 \
  --json name,description,licenseInfo,repositoryTopics,latestRelease,pushedAt,isFork,primaryLanguage \
  > "${TMPDIR:-/tmp}/packaging-repos.json" || { echo "gh repo list failed"; exit 1; }

# Workflow presence needs a second call per repo (.github/workflows on the default branch).
: > "${TMPDIR:-/tmp}/packaging-ci.tsv"
while IFS=$'\t' read -r name branch; do
  n=$(gh api "repos/$OWNER/$name/contents/.github/workflows?ref=$branch" \
        --jq 'if type == "array" then length else 0 end' 2>/dev/null)
  case "$n" in ''|*[!0-9]*) n=0 ;; esac
  printf '%s\t%s\n' "$name" "$n" >> "${TMPDIR:-/tmp}/packaging-ci.tsv"
done < <(gh repo list "$OWNER" --limit 100 --json name,defaultBranchRef \
  --jq '.[] | "\(.name)\t\(.defaultBranchRef.name // "main")"')

python3 - "$OWNER" <<'PY'
import json, sys, os

owner = sys.argv[1]
repos = json.load(open(os.path.join(os.environ.get("TMPDIR", "/tmp"), "packaging-repos.json")))
ci = {}
path = os.path.join(os.environ.get("TMPDIR", "/tmp"), "packaging-ci.tsv")
if os.path.exists(path):
    for line in open(path):
        if "\t" in line:
            name, n = line.rstrip("\n").split("\t")
            try:
                ci[name] = int(n)
            except ValueError:
                ci[name] = 0

SKIP_FORKS = True
rows = []
for r in sorted(repos, key=lambda x: x["name"]):
    if SKIP_FORKS and r.get("isFork"):
        continue
    name = r["name"]
    desc = "yes" if (r.get("description") or "").strip() else "no"
    lic = ((r.get("licenseInfo") or {}).get("spdxId")
           or (r.get("licenseInfo") or {}).get("key")
           or "no").upper()
    topics = len(r.get("repositoryTopics") or [])
    rel = (r.get("latestRelease") or {}).get("tagName") or "-"
    workflows = ci.get(name, 0)
    rows.append((name, desc, lic, topics, workflows, rel))

w = max(len("REPO"), max((len(r[0]) for r in rows), default=4))
print(f"{'REPO':<{w}}  {'DESC':<4} {'LICENCE':<14} {'TOPICS':>6} {'CI':>3} {'RELEASE':<12}")
print(f"{'-'*w}  {'-'*4} {'-'*14} {'-'*6} {'-'*3} {'-'*12}")
for name, desc, lic, topics, wf, rel in rows:
    print(f"{name:<{w}}  {desc:<4} {lic:<14} {topics:>6} {wf:>3} {rel:<12}")

n = len(rows)
d = sum(1 for r in rows if r[1] == "yes")
l = sum(1 for r in rows if r[2] != "NO")
t = sum(1 for r in rows if r[3] >= 5)
c = sum(1 for r in rows if r[4] >= 1)
rel = sum(1 for r in rows if r[5] != "-")

def line(label, got, target):
    mark = "OK " if got >= target else "   "
    print(f"  {mark}{label:<14} {got:>2}/{n}   target {target}/{n}")

print()
print("--------------------------------------------------------------")
line("descriptions", d, n)
line("licences", l, n)
line("topics >= 5", t, n)
line("CI workflows", c, 5)
line("releases", rel, 6)
print("--------------------------------------------------------------")
print("Not machine-checkable: live demo links, README screenshots, pinned repos.")
PY
