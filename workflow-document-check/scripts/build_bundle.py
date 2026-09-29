#!/usr/bin/env python3
"""Build the standalone Python validator archive."""

from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import zipapp


SKILL = Path(__file__).resolve().parents[1]
OUTPUT = SKILL / "dist" / "check_workflow_docs.pyz"


def main() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        target = Path(temporary) / "package"
        target.mkdir()
        requirements = SKILL / "requirements-build.txt"
        if shutil.which("uv"):
            command = [
                "uv", "pip", "install", "--target", str(target),
                "--python", sys.executable, "--no-compile", "--link-mode=copy",
                "-r", str(requirements),
            ]
        else:
            command = [
                sys.executable, "-m", "pip", "install", "--target", str(target),
                "--no-compile", "-r", str(requirements),
            ]
        env = dict(os.environ)
        env["UV_CACHE_DIR"] = str(Path(temporary) / "uv-cache")
        subprocess.run(command, check=True, env=env)
        shutil.copyfile(SKILL / "scripts" / "validate.py", target / "__main__.py")
        OUTPUT.parent.mkdir(exist_ok=True)
        zipapp.create_archive(target, target=OUTPUT, compressed=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
