# Sandbox Security Baseline

This project runs untrusted code only in a constrained sandbox.

## Required Runtime Controls

- Container runtime: Docker with gVisor (`runsc`).
- Runtime can be overridden for local fallback with `SANDBOX_RUNTIME` (default `runsc`).
- No network: `--network=none`.
- Non-root user inside container.
- Read-only root filesystem.
- Resource limits: CPU, memory, pids.
- Hard timeout per execution.
- Temporary workspace mounted for source and artifacts.

## Languages

- C (`gcc`)
- C++ (`g++`)
- Java (`javac` + `java`)

## Execution Contract

Return structured result for every run:

- `compile_ok`
- `stdout`
- `stderr`
- `exit_code`
- `time_ms`
- `memory_kb`
- `timeout`
