#!/usr/bin/env bash

set -euo pipefail

runtime="${SANDBOX_RUNTIME:-runsc}"
echo "using runtime: ${runtime}"

PYTHONPATH=. SANDBOX_RUNTIME="${runtime}" uv run --with pydantic python3 - <<'PY'
from apps.api.app.services.sandbox import execute_code

cases = {
    "c": "#include <stdio.h>\nint main(void){puts(\"c-ok\");return 0;}\n",
    "cpp": "#include <iostream>\nint main(){std::cout<<\"cpp-ok\\n\";return 0;}\n",
    "java": "public class Main { public static void main(String[] args){ System.out.println(\"java-ok\"); } }\n",
}

for lang, code in cases.items():
    result = execute_code(lang, code)
    print(lang, result.compile_ok, result.exit_code, result.stdout.strip())
PY
