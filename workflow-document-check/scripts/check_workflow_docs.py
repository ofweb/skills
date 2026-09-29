#!/usr/bin/env python3
"""Run the workflow document validator from the existing command path."""

from pathlib import Path
import subprocess
import sys


def main() -> int:
    script = Path(__file__).with_name("check_workflow_docs.mjs")
    if not (script.parent.parent / "node_modules").is_dir():
        print("Run npm ci in the workflow-document-check skill directory.", file=sys.stderr)
        return 2
    try:
        return subprocess.call(["node", str(script), *sys.argv[1:]])
    except FileNotFoundError:
        print("Node.js is required for workflow-document-check.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
