# GitHub Pages Frontend Deployment Design

## Goal

Deploy the existing frontend (`apps/web`) to GitHub Pages while keeping the backend sandbox service local or separately hosted, and make API target configurable by environment.

## Scope

- In scope:
  - Frontend static deployment to GitHub Pages
  - Build-time API base URL injection via Vite environment variables
  - CI pipeline for test, build, and publish
  - Basic rollback and release safety process
- Out of scope:
  - Backend cloud hosting
  - Multi-environment backend infrastructure
  - Authentication and private access control

## Constraints and Decisions

- Repository remains single source of truth for code and deployment workflow.
- Frontend must not hardcode API base URL.
- API base is provided using `VITE_API_BASE_URL` in build pipeline.
- Deployment target is GitHub Pages, with artifacts published from CI only.
- No secrets in frontend bundle; only public config via `VITE_*` variables.

## Architecture

1. Developer pushes frontend/backend code to repository branch (`dev` as base integration branch).
2. GitHub Actions workflow runs on configured branch/path triggers.
3. Workflow installs dependencies, runs frontend tests, then builds frontend with `VITE_API_BASE_URL`.
4. Build output (`apps/web/dist`) is published to `gh-pages` branch.
5. GitHub Pages serves static assets from `gh-pages`.
6. Browser calls backend using injected API base URL.

## Frontend Configuration Design

- Replace hardcoded API endpoint in `apps/web/src/api.js` with:
  - `const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";`
- Local developer setup:
  - `.env.local` in `apps/web` can define `VITE_API_BASE_URL` for local runs.
- CI setup:
  - Workflow injects `VITE_API_BASE_URL` from repository/environment variable at build time.

## CI/CD Workflow Design

Recommended workflow steps:

1. `actions/checkout`
2. `actions/setup-node` (Node 20)
3. `npm --prefix apps/web ci`
4. `npm --prefix apps/web test`
5. `npm --prefix apps/web run build` (with `VITE_API_BASE_URL` env)
6. Deploy `apps/web/dist` to `gh-pages` using `peaceiris/actions-gh-pages`

Deployment rules:

- If tests or build fail, deployment is skipped.
- Deploy only from trusted branch (default `dev`) to reduce accidental publish.
- Keep deployment action idempotent: each successful run replaces static site with current artifact.

## Security and Reliability

- Do not place sensitive tokens in any `VITE_*` variable.
- If backend is public, configure backend CORS to allow GitHub Pages origin.
- Keep branch protection on `dev` (PR review + status checks).
- Treat `gh-pages` as generated output branch; do not manually edit.

## Rollback Plan

- Primary rollback: redeploy a previous known-good commit by re-running workflow on that commit.
- Secondary rollback: revert problematic commit in `dev`, then allow CI to publish corrected artifact.
- Since pages is static, rollback does not require database migration handling.

## Verification Plan

- CI verification:
  - Frontend tests pass in workflow before deploy.
  - Build succeeds with injected `VITE_API_BASE_URL`.
- Post-deploy smoke checks:
  - Open Pages URL and verify app loads.
  - Trigger one API call and confirm request target matches configured base URL.
  - Confirm focus-mode default behavior remains unchanged.

## Implementation Notes

- Keep changes minimal and isolated:
  - `apps/web/src/api.js` (env-based API base)
  - `apps/web/.env.example` (optional guidance file)
  - `.github/workflows/deploy-web.yml` (build and publish)
  - `README.md` deployment section updates
- Prefer explicit docs for local vs CI variables to avoid configuration drift.
