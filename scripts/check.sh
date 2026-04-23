#!/usr/bin/env bash

set -euo pipefail

PYTHONPATH=. uv run --with fastapi --with pydantic --with pytest --with httpx pytest apps/api/tests -q

echo "backend checks passed"

if [ -d "apps/web/node_modules" ]; then
  npm --prefix apps/web test
  echo "frontend tests passed"
else
  echo "apps/web dependencies missing, run: npm --prefix apps/web install"
fi

if command -v docker >/dev/null 2>&1; then
  if docker image inspect sandbox-runner:latest >/dev/null 2>&1; then
    echo "sandbox image found: sandbox-runner:latest"
    if command -v runsc >/dev/null 2>&1; then
      SANDBOX_RUNTIME=runsc bash scripts/sandbox-smoke.sh
    else
      echo "runsc not found, fallback smoke with SANDBOX_RUNTIME=runc"
      SANDBOX_RUNTIME=runc bash scripts/sandbox-smoke.sh
    fi
  else
    echo "sandbox image missing, run: bash scripts/sandbox-build.sh"
  fi
else
  echo "docker not found, sandbox runtime smoke skipped"
fi
