# Repository Hardening Checklist (Public Launch)

Use this checklist in **GitHub → Settings** to lock down quality and security for public contributions.

## 1) General settings

- [ ] Enable **Issues** and **Pull Requests**
- [ ] Disable **Projects** if unused (optional)
- [ ] Set default branch to `main`
- [ ] Enable **Automatically delete head branches**
- [ ] Set merge strategy:
  - [ ] Enable **Squash merge**
  - [ ] Disable merge commits/rebase merge if you want linear history (optional)

## 2) Branch protection (`main`)

Create a ruleset or branch protection for `main`:

- [ ] Require a pull request before merging
- [ ] Require approvals: **1+**
- [ ] Dismiss stale approvals on new commits
- [ ] Require conversation resolution before merging
- [ ] Require status checks to pass
  - [ ] Add required check: **`CI Required Check`**
- [ ] Require branches to be up to date before merging
- [ ] Include administrators (recommended)
- [ ] Restrict force pushes and deletions

> Why one required check? Matrix jobs create multiple dynamic check names. `CI Required Check` is stable and easier to enforce.

## 3) Security settings

In **Settings → Security & analysis**:

- [ ] Enable **Dependency graph**
- [ ] Enable **Dependabot alerts**
- [ ] Enable **Dependabot security updates**
- [ ] Enable **Secret scanning**
- [ ] Enable **Push protection** for secret scanning
- [ ] Enable **Code scanning default setup** (CodeQL) if available

## 4) Actions hardening

In **Settings → Actions → General**:

- [ ] Allow actions from GitHub and verified creators (or stricter, per preference)
- [ ] Require approval for first-time contributors
- [ ] Set workflow permissions to **Read repository contents**
- [ ] Disable “Allow GitHub Actions to create and approve pull requests” unless required

## 5) Community profile completeness

In **Insights → Community Standards**:

- [x] `README.md`
- [x] `LICENSE`
- [x] `CONTRIBUTING.md`
- [x] `CODE_OF_CONDUCT.md`
- [x] `SECURITY.md`
- [x] Issue templates
- [x] Pull request template

## 6) Optional portfolio polish

- [ ] Add topic tags (e.g., `mcp`, `fastapi`, `rapid7`, `security`, `python`)
- [ ] Add social preview image
- [ ] Pin this repo on your profile
- [ ] Add a short demo GIF/video in `README.md`
- [ ] Create `CHANGELOG.md` release entries and GitHub Releases

## 7) Post-launch maintenance rhythm

- [ ] Triage issues weekly
- [ ] Review Dependabot PRs weekly
- [ ] Keep action SHAs and dependency pins updated monthly
- [ ] Cut tagged releases for meaningful milestones
