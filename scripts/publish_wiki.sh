#!/usr/bin/env bash
set -euo pipefail

# Sync docs/wiki/*.md into the GitHub Wiki repository.
#
# Usage:
#   scripts/publish_wiki.sh [--repo owner/name] [--push] [--clean]
#
# Defaults:
#   - preview only (no push)
#   - no delete of unmanaged files in Wiki

REPO_SLUG=""
PUSH=false
CLEAN=false
SOURCE_DIR="docs/wiki"

usage() {
  cat <<'EOF'
Sync docs/wiki markdown files to GitHub Wiki.

Usage:
  scripts/publish_wiki.sh [--repo owner/name] [--push] [--clean]

Options:
  --repo owner/name   GitHub repo slug (auto-detected from origin if omitted)
  --push              Push commit to Wiki remote
  --clean             Remove tracked markdown files in Wiki that are not present in docs/wiki
  -h, --help          Show this help

Examples:
  scripts/publish_wiki.sh
  scripts/publish_wiki.sh --repo SecuritahGuy/rapid7-mcp --push
  scripts/publish_wiki.sh --push --clean
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      REPO_SLUG="${2:-}"
      shift 2
      ;;
    --push)
      PUSH=true
      shift
      ;;
    --clean)
      CLEAN=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Source directory not found: $SOURCE_DIR" >&2
  exit 1
fi

if [[ -z "$REPO_SLUG" ]]; then
  origin_url="$(git remote get-url origin 2>/dev/null || true)"
  if [[ -z "$origin_url" ]]; then
    echo "Could not auto-detect repo from git origin. Use --repo owner/name." >&2
    exit 1
  fi

  # Supports:
  #   git@github.com:owner/repo.git
  #   https://github.com/owner/repo.git
  REPO_SLUG="$(printf '%s' "$origin_url" | sed -E 's#(git@github.com:|https://github.com/)##; s#\.git$##')"
fi

if [[ ! "$REPO_SLUG" =~ ^[^/]+/[^/]+$ ]]; then
  echo "Invalid repo slug: $REPO_SLUG (expected owner/name)" >&2
  exit 1
fi

WIKI_URL="https://github.com/${REPO_SLUG}.wiki.git"
AUTH_TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}"

if [[ -n "$AUTH_TOKEN" ]]; then
  WIKI_URL_AUTH="https://x-access-token:${AUTH_TOKEN}@github.com/${REPO_SLUG}.wiki.git"
else
  WIKI_URL_AUTH="$WIKI_URL"
fi

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

WIKI_DIR="$TMP_DIR/wiki"

echo "==> Repo:          $REPO_SLUG"
echo "==> Source:        $SOURCE_DIR"
echo "==> Wiki remote:   $WIKI_URL"
echo "==> Push enabled:  $PUSH"
echo "==> Clean mode:    $CLEAN"

if git clone "$WIKI_URL_AUTH" "$WIKI_DIR" >/dev/null 2>&1; then
  echo "==> Cloned existing Wiki repository"
else
  echo "==> Wiki clone failed; initializing local wiki repo scaffold"
  mkdir -p "$WIKI_DIR"
  git -C "$WIKI_DIR" init >/dev/null
  git -C "$WIKI_DIR" remote add origin "$WIKI_URL_AUTH"
fi

# Ensure we can commit even in clean CI/local environments.
if ! git -C "$WIKI_DIR" config user.email >/dev/null; then
  git -C "$WIKI_DIR" config user.email "wiki-sync@users.noreply.github.com"
fi
if ! git -C "$WIKI_DIR" config user.name >/dev/null; then
  git -C "$WIKI_DIR" config user.name "wiki-sync-bot"
fi

# Copy markdown pages from source to wiki root.
find "$SOURCE_DIR" -maxdepth 1 -type f -name '*.md' -print0 | while IFS= read -r -d '' f; do
  cp "$f" "$WIKI_DIR/$(basename "$f")"
done

if [[ "$CLEAN" == true ]]; then
  echo "==> Cleaning tracked markdown files not present in source"
  while IFS= read -r tracked; do
    bn="$(basename "$tracked")"
    if [[ ! -f "$SOURCE_DIR/$bn" ]]; then
      git -C "$WIKI_DIR" rm -f "$tracked" >/dev/null 2>&1 || true
    fi
  done < <(git -C "$WIKI_DIR" ls-files '*.md')
fi

# Stage and review changes.
git -C "$WIKI_DIR" add -A

if git -C "$WIKI_DIR" diff --cached --quiet; then
  echo "==> No wiki changes detected"
  exit 0
fi

echo "==> Pending wiki changes:"
git -C "$WIKI_DIR" --no-pager diff --cached --name-status

commit_msg="docs(wiki): sync from docs/wiki ($(date -u +%Y-%m-%dT%H:%M:%SZ))"
git -C "$WIKI_DIR" commit -m "$commit_msg" >/dev/null

echo "==> Created commit"

if [[ "$PUSH" == true ]]; then
  echo "==> Pushing to $WIKI_URL"
  # GitHub Wiki repositories use master by default.
  git -C "$WIKI_DIR" push origin HEAD:master
  echo "==> Wiki publish complete"
else
  echo "==> Dry run complete (no push). Re-run with --push to publish."
fi
