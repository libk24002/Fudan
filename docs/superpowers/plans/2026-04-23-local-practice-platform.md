# Local Practice Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local single-user training platform with sandbox practice, AI review, and automatic repository archiving.

**Architecture:** FastAPI orchestrates problem lifecycle, sandbox execution, AI review, and archive writes. React frontend provides problem submission, practice, finish, and archive actions. Docker + gVisor executes untrusted code for C/C++/Java safely.

**Tech Stack:** Python 3.12, FastAPI, SQLite, React+TypeScript, Docker, gVisor, pytest.

---

### Task 1: Backend skeleton and health endpoint

**Files:**
- Create: `apps/api/main.py`
- Create: `apps/api/tests/test_health.py`

- [ ] **Step 1: Write failing test**

```python
from fastapi.testclient import TestClient
from apps.api.main import app

def test_health_ok():
    client = TestClient(app)
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_health.py -q`
Expected: FAIL (module or route missing)

- [ ] **Step 3: Implement minimal endpoint**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "ok"}
```

- [ ] **Step 4: Run test to verify pass**

Run: `pytest apps/api/tests/test_health.py -q`
Expected: `1 passed`

- [ ] **Step 5: Commit**

Run: `git add apps/api/main.py apps/api/tests/test_health.py && git commit -m "feat(api): bootstrap fastapi health endpoint"`

### Task 2: State machine and problem lifecycle

**Files:**
- Create: `apps/api/app/state_machine.py`
- Create: `apps/api/tests/test_state_machine.py`

- [ ] Write failing transition tests.
- [ ] Implement transitions: `created -> practicing -> finished -> archiving -> archived` with rollback `archiving -> practicing`.
- [ ] Run tests and commit.

### Task 3: Sandbox contract for C/C++/Java

**Files:**
- Create: `apps/api/app/services/sandbox.py`
- Create: `infra/sandbox/Dockerfile`
- Create: `apps/api/tests/test_sandbox_contract.py`

- [ ] Define unified execution response schema.
- [ ] Implement language command mapping (`c/cpp/java`).
- [ ] Add gVisor-compatible runtime assumptions and limits placeholders.
- [ ] Run tests and commit.

### Task 4: API routes for problem, execute, review, archive

**Files:**
- Create: `apps/api/app/routes/problems.py`
- Create: `apps/api/app/routes/sandbox.py`
- Create: `apps/api/app/routes/review.py`
- Modify: `apps/api/main.py`

- [ ] Add create/list/detail/finish APIs.
- [ ] Add sandbox execute API.
- [ ] Add review and archive APIs with finish+PASS gate.
- [ ] Add tests, run, and commit.

### Task 5: Repository writer and index builder

**Files:**
- Create: `apps/api/app/services/repo_writer.py`
- Create: `apps/api/app/services/indexer.py`
- Create: `apps/api/tests/test_repo_writer.py`
- Create: `apps/api/tests/test_indexer.py`

- [ ] Write archive output files: `solution.c`, `README.md`, `meta.yaml`, `review.md`.
- [ ] Ensure user thinking is included in README summary.
- [ ] Generate `index/by-module.md` and `index/by-c-topic.md`.
- [ ] Run tests and commit.

### Task 6: Frontend MVP for practice and two-button flow

**Files:**
- Create: `apps/web/src/pages/PracticePage.tsx`
- Create: `apps/web/src/pages/ProblemListPage.tsx`
- Create: `apps/web/src/pages/ProblemDetailPage.tsx`
- Create: `apps/web/src/lib/api.ts`

- [ ] Implement problem submission and free practice page.
- [ ] Implement execute/finish/archive buttons.
- [ ] Disable archive until finish is done.
- [ ] Add tests and commit.

### Task 7: Security hardening and final verification

**Files:**
- Create: `infra/sandbox/security.md`
- Create: `scripts/check.sh`

- [ ] Enforce no-network, non-root, timeout, memory and pids limits.
- [ ] Add smoke checks for C/C++/Java execution.
- [ ] Run final checks and commit.
