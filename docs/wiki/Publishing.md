# Publishing the Wiki

This repo keeps wiki content versioned under `docs/wiki/`.

Use the publisher script to sync those pages into the GitHub Wiki repository.

## Script

- `scripts/publish_wiki.sh`

## Automated publishing (GitHub Actions)

Workflow: `.github/workflows/wiki-publish.yml`

- Pull requests touching wiki files run a **preview only** sync.
- Pushes to `main` touching wiki files trigger publish, but are gated by environment approval.
- Manual dispatch supports preview or publish with optional clean mode.

### Required one-time setup

In GitHub repository settings, create an environment named `wiki-publish` and add required reviewers.

This provides the manual approval gate before any wiki push occurs.

## Recommended flow

1. Review changes locally in `docs/wiki/`.
2. Run a preview (no push):
   - `scripts/publish_wiki.sh`
3. Publish when ready:
   - `scripts/publish_wiki.sh --push`

## Options

- `--repo owner/name` — override repo slug (auto-detected from git origin by default)
- `--push` — publish to GitHub Wiki remote
- `--clean` — remove tracked markdown files in Wiki that are no longer in `docs/wiki/`

## Examples

- Preview:
  - `scripts/publish_wiki.sh`
- Publish:
  - `scripts/publish_wiki.sh --push`
- Publish and remove stale pages:
  - `scripts/publish_wiki.sh --push --clean`

## Notes

- The script is **dry-run by default** (it commits in a temp clone but does not push).
- If your Wiki has never been initialized on GitHub, create one page once in the GitHub UI, then re-run publish.
- The script targets the Wiki default branch (`master`).
- In CI, the script uses `GITHUB_TOKEN` for authenticated clone/push of the wiki repository.
- If the Wiki repository is missing, publish can be configured to skip gracefully by setting `ALLOW_MISSING_WIKI=true`.
