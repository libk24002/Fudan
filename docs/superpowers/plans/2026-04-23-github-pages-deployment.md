# GitHub Pages Frontend Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy `apps/web` to GitHub Pages with build-time configurable API endpoint while preserving local development defaults.

**Architecture:** The frontend reads `VITE_API_BASE_URL` during build, with local fallback to `http://127.0.0.1:8000`. GitHub Actions runs frontend tests and build, then publishes `apps/web/dist` to `gh-pages`. Vite `base` is set for project Pages so static assets resolve under `/Fudan/`.

**Tech Stack:** React 18, Vite 5, Vitest, GitHub Actions, peaceiris/actions-gh-pages.

---

## File Structure and Responsibilities

- Modify: `apps/web/src/api.js`
  - Replace hardcoded API base with `import.meta.env.VITE_API_BASE_URL` fallback.
- Create: `apps/web/.env.example`
  - Document frontend runtime build variables.
- Modify: `apps/web/vite.config.js`
  - Configure `base` for GitHub Pages (`/Fudan/`) while keeping local `/`.
- Create: `.github/workflows/deploy-web.yml`
  - CI pipeline for test/build/deploy to `gh-pages`.
- Modify: `README.md`
  - Add GitHub Pages deployment section and variable setup.

### Task 1: Make API base URL environment-configurable

**Files:**
- Modify: `apps/web/src/api.js`
- Test (add): `apps/web/src/api.test.js`

- [ ] **Step 1: Write the failing test for env API base resolution**

```js
import { describe, expect, it, vi } from "vitest";

describe("request API base", () => {
  it("uses VITE_API_BASE_URL when provided", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => ({ ok: true }) }));
    vi.stubEnv("VITE_API_BASE_URL", "https://api.example.com");

    const { request } = await import("./api.js");
    await request("/api/health");

    expect(fetch).toHaveBeenCalledWith("https://api.example.com/api/health", expect.any(Object));
    vi.unstubAllGlobals();
    vi.unstubAllEnvs();
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npm --prefix apps/web test -- src/api.test.js`
Expected: FAIL because current API base is hardcoded.

- [ ] **Step 3: Implement env-based API base with local fallback**

```js
const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.detail || response.statusText);
  }
  return payload;
}
```

- [ ] **Step 4: Add or adjust test to avoid module cache cross-test pollution**

```js
import { beforeEach, describe, expect, it, vi } from "vitest";

describe("request API base", () => {
  beforeEach(() => {
    vi.resetModules();
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
  });

  it("uses fallback when env is absent", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => ({ ok: true }) }));
    const { request } = await import("./api.js");
    await request("/api/health");
    expect(fetch).toHaveBeenCalledWith("http://127.0.0.1:8000/api/health", expect.any(Object));
  });

  it("uses VITE_API_BASE_URL when provided", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => ({ ok: true }) }));
    vi.stubEnv("VITE_API_BASE_URL", "https://api.example.com");
    const { request } = await import("./api.js");
    await request("/api/health");
    expect(fetch).toHaveBeenCalledWith("https://api.example.com/api/health", expect.any(Object));
  });
});
```

- [ ] **Step 5: Run tests to verify pass**

Run: `npm --prefix apps/web test -- src/api.test.js src/App.test.jsx`
Expected: PASS for all tests.

- [ ] **Step 6: Commit**

```bash
git add apps/web/src/api.js apps/web/src/api.test.js
git commit -m "feat(web): support env-based API base URL"
```

### Task 2: Configure Vite base path for GitHub Pages

**Files:**
- Modify: `apps/web/vite.config.js`
- Test/Verify: `npm --prefix apps/web run build`

- [ ] **Step 1: Update Vite config with base path logic**

```js
import { defineConfig } from "vite";

const isCI = process.env.GITHUB_ACTIONS === "true";

export default defineConfig({
  base: isCI ? "/Fudan/" : "/",
  test: {
    environment: "jsdom",
    setupFiles: "./src/test/setup.js"
  }
});
```

- [ ] **Step 2: Run build locally to verify output still builds**

Run: `npm --prefix apps/web run build`
Expected: `vite build` exits with code 0.

- [ ] **Step 3: Commit**

```bash
git add apps/web/vite.config.js
git commit -m "build(web): set GitHub Pages base path for CI builds"
```

### Task 3: Add GitHub Actions deploy workflow

**Files:**
- Create: `.github/workflows/deploy-web.yml`

- [ ] **Step 1: Create workflow with test/build/deploy jobs**

```yaml
name: Deploy Web to GitHub Pages

on:
  push:
    branches: ["dev"]
    paths:
      - "apps/web/**"
      - ".github/workflows/deploy-web.yml"
  workflow_dispatch:

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      VITE_API_BASE_URL: ${{ vars.VITE_API_BASE_URL }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
          cache-dependency-path: apps/web/package-lock.json

      - name: Install dependencies
        run: npm --prefix apps/web ci

      - name: Run tests
        run: npm --prefix apps/web test

      - name: Build
        run: npm --prefix apps/web run build

      - name: Deploy to gh-pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: apps/web/dist
```

- [ ] **Step 2: Validate workflow syntax quickly**

Run: `git diff -- .github/workflows/deploy-web.yml`
Expected: YAML includes `push`, `workflow_dispatch`, test, build, deploy steps.

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/deploy-web.yml
git commit -m "ci(web): add GitHub Pages deploy workflow"
```

### Task 4: Document local and GitHub configuration

**Files:**
- Create: `apps/web/.env.example`
- Modify: `README.md`

- [ ] **Step 1: Add frontend env example file**

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
```

- [ ] **Step 2: Update README with deployment instructions**

```md
## 部署前端到 GitHub Pages

1. 在仓库 Settings -> Pages 中启用 GitHub Pages（来源使用 `gh-pages` 分支）。
2. 在仓库 Settings -> Secrets and variables -> Actions -> Variables 中新增：
   - `VITE_API_BASE_URL`：前端请求后端的基础地址（公开变量）。
3. 推送 `dev` 分支触发 `.github/workflows/deploy-web.yml`。
4. CI 通过后自动发布 `apps/web/dist` 到 `gh-pages`。

本地开发可复制 `apps/web/.env.example` 为 `apps/web/.env.local` 并按需修改。
```

- [ ] **Step 3: Run full project checks**

Run: `bash scripts/check.sh`
Expected: backend tests pass, frontend tests pass, sandbox smoke passes (runsc or runc fallback).

- [ ] **Step 4: Commit**

```bash
git add apps/web/.env.example README.md
git commit -m "docs(web): add GitHub Pages deployment and env setup guide"
```

### Task 5: End-to-end deployment validation

**Files:**
- Verify only (no mandatory code changes)

- [ ] **Step 1: Push branch and open PR to `dev`**

Run: `git push -u origin <branch-name>`
Expected: branch pushed successfully.

- [ ] **Step 2: Merge to `dev` after review**

Run: GitHub PR merge flow
Expected: merge commit appears on `dev`.

- [ ] **Step 3: Verify Pages deployment output**

Run: check Actions logs and open Pages URL
Expected:
- Deploy workflow succeeds.
- Frontend loads without missing asset errors.
- API request target uses configured `VITE_API_BASE_URL`.

- [ ] **Step 4: Rollback drill (optional but recommended)**

Run: re-run a previous known-good deploy workflow if needed
Expected: Pages content returns to known-good version.
