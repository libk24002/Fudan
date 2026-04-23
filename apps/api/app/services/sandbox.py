from __future__ import annotations

import subprocess
import tempfile
import time
import os
from pathlib import Path

from pydantic import BaseModel


SUPPORTED_LANGUAGES = {"c", "cpp", "java"}


LANG_COMMANDS = {
    "c": {
        "source_file": "main.c",
        "compile": ["gcc", "main.c", "-O2", "-std=c11", "-o", "main"],
        "run": ["./main"],
    },
    "cpp": {
        "source_file": "main.cpp",
        "compile": ["g++", "main.cpp", "-O2", "-std=c++17", "-o", "main"],
        "run": ["./main"],
    },
    "java": {
        "source_file": "Main.java",
        "compile": ["javac", "Main.java"],
        "run": ["java", "Main"],
    },
}


class SandboxResult(BaseModel):
    compile_ok: bool
    stdout: str
    stderr: str
    exit_code: int
    time_ms: int
    memory_kb: int
    timeout: bool


def validate_language(language: str) -> str:
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language}")
    return language


def _compose_docker_command(workdir: Path, timeout_seconds: int) -> list[str]:
    runtime = os.environ.get("SANDBOX_RUNTIME", "runsc")
    uid = os.getuid()
    gid = os.getgid()
    return [
        "docker",
        "run",
        "--rm",
        f"--runtime={runtime}",
        "--network=none",
        "--read-only",
        "--pids-limit=64",
        "--memory=256m",
        "--cpus=1",
        "--security-opt=no-new-privileges",
        "--user",
        f"{uid}:{gid}",
        "-v",
        f"{workdir}:/workspace:rw",
        "-w",
        "/workspace",
        "sandbox-runner:latest",
        "timeout",
        str(timeout_seconds),
    ]


def execute_code(language: str, code: str, stdin: str = "", timeout_seconds: int = 2) -> SandboxResult:
    language = validate_language(language)
    commands = LANG_COMMANDS[language]

    with tempfile.TemporaryDirectory(prefix="practice-sandbox-") as td:
        workdir = Path(td)
        source_path = workdir / commands["source_file"]
        source_path.write_text(code, encoding="utf-8")

        docker_base = _compose_docker_command(workdir, timeout_seconds)

        compile_start = time.time()
        compile_proc = subprocess.run(
            docker_base + commands["compile"],
            capture_output=True,
            text=True,
            check=False,
        )
        compile_elapsed = int((time.time() - compile_start) * 1000)
        if compile_proc.returncode != 0:
            return SandboxResult(
                compile_ok=False,
                stdout=compile_proc.stdout,
                stderr=compile_proc.stderr,
                exit_code=compile_proc.returncode,
                time_ms=compile_elapsed,
                memory_kb=0,
                timeout=False,
            )

        run_start = time.time()
        run_proc = subprocess.run(
            docker_base + commands["run"],
            input=stdin,
            capture_output=True,
            text=True,
            check=False,
        )
        run_elapsed = int((time.time() - run_start) * 1000)

        return SandboxResult(
            compile_ok=True,
            stdout=run_proc.stdout,
            stderr=run_proc.stderr,
            exit_code=run_proc.returncode,
            time_ms=run_elapsed,
            memory_kb=0,
            timeout=run_proc.returncode == 124,
        )
