"""Tests for the Markdown prose boundary and command status."""

from __future__ import annotations

import os
import runpy
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent / "concise-prose"
MODULE = runpy.run_path(str(SKILL_DIR / "prose-check"), run_name="prose_check_test")


@unittest.skipUnless(shutil.which("cmark"), "cmark is required")
class MarkdownProseTests(unittest.TestCase):
    def test_code_and_link_target_are_absent_without_shifting_offsets(self) -> None:
        source = (
            "# Café\n\nUse `utilize` and [the file](https://example.com).\n\n"
            "```text\nleverage synergy\n```\n"
        )
        prose = MODULE["prose_only"](source)

        self.assertEqual(len(prose), len(source))
        self.assertEqual(prose.index("Café"), source.index("Café"))
        self.assertEqual(prose.index("the file"), source.index("the file"))
        for hidden in ("utilize", "https://example.com", "leverage synergy"):
            self.assertNotIn(hidden, prose)


@unittest.skipUnless(shutil.which("cmark"), "cmark is required")
class CommandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        checker = self.directory / "ste100"
        checker.write_text(
            "#!/usr/bin/env python3\n"
            "import sys\n"
            "text = sys.stdin.read()\n"
            "print('STE text:', repr(text))\n"
            "sys.exit(1 if 'BAD' in text else 0)\n",
            encoding="utf-8",
        )
        checker.chmod(0o755)
        vale = self.directory / "vale"
        vale.write_text(
            "#!/usr/bin/env python3\n"
            "import os, sys\n"
            "print('VALE RAN')\n"
            "sys.exit(int(os.environ.get('FAKE_VALE_STATUS', '0')))\n",
            encoding="utf-8",
        )
        vale.chmod(0o755)
        self.env = dict(os.environ, PATH=f"{self.directory}:{os.environ['PATH']}")

    def run_tool(self, *args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(SKILL_DIR / "prose-check"), *args],
            input=input_text,
            text=True,
            capture_output=True,
            env=self.env,
            check=False,
        )

    def test_stdin_ignores_code_but_checks_prose(self) -> None:
        passed = self.run_tool(input_text="Use the file.\n\n```text\nBAD\n```\n")
        self.assertEqual(passed.returncode, 0, passed.stderr)
        self.assertNotIn("BAD", passed.stdout)
        self.assertLess(passed.stdout.index("STE100 =="), passed.stdout.index("Vale =="))

        failed = self.run_tool(input_text="BAD prose.\n")
        self.assertEqual(failed.returncode, 1, failed.stderr)
        self.assertNotIn("Vale ==", failed.stdout)

    def test_vale_failure_after_ste100_passes(self) -> None:
        self.env["FAKE_VALE_STATUS"] = "1"
        result = self.run_tool(input_text="Use the file.\n")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertLess(result.stdout.index("STE100 =="), result.stdout.index("Vale =="))

    @unittest.skipUnless(shutil.which("vale"), "Vale is required")
    def test_real_vale_checks_stdin_after_ste100_passes(self) -> None:
        tools_dir = self.directory / "real-vale"
        tools_dir.mkdir()
        (tools_dir / "ste100").symlink_to(self.directory / "ste100")
        self.env["PATH"] = f"{tools_dir}:{os.environ['PATH']}"

        result = self.run_tool(input_text="Use the relevant file.\n")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("Empty qualifier", result.stdout)

    def test_multiple_files_return_failure_if_one_fails(self) -> None:
        first = self.directory / "first.md"
        second = self.directory / "second.md"
        first.write_text("BAD prose.\n", encoding="utf-8")
        second.write_text("Use the file.\n", encoding="utf-8")

        result = self.run_tool(str(first), str(second))
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(f"== {first}: STE100 ==", result.stdout)
        self.assertNotIn(f"== {first}: Vale ==", result.stdout)
        self.assertIn(f"== {second}: STE100 ==", result.stdout)
        self.assertIn(f"== {second}: Vale ==", result.stdout)
        self.assertLess(result.stdout.index(f"== {first}: STE100 =="), result.stdout.index(f"== {second}: Vale =="))

    def test_missing_checker_is_a_tool_failure(self) -> None:
        without_checker = self.directory / "without-checker"
        without_checker.mkdir()
        (without_checker / "cmark").symlink_to(shutil.which("cmark"))
        (without_checker / "vale").symlink_to(self.directory / "vale")
        (without_checker / "python3").symlink_to("/usr/bin/python3")
        self.env["PATH"] = str(without_checker)

        result = self.run_tool(input_text="Use the file.\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing command: ste100", result.stderr)


if __name__ == "__main__":
    unittest.main()
