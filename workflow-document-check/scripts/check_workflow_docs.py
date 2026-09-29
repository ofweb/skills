#!/usr/bin/env python3
"""Run the bundled workflow document validator."""

from pathlib import Path
import subprocess
import sys


def main() -> int:
    script = Path(__file__).resolve().parent.parent / "dist" / "check_workflow_docs.pyz"
    if not script.is_file():
        print("The bundled workflow validator is missing.", file=sys.stderr)
        return 2
    try:
        return subprocess.call([sys.executable, str(script), *sys.argv[1:]])
    except FileNotFoundError:
        print("Python is required for workflow-document-check.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
