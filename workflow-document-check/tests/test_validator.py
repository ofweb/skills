import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
COMMAND = SKILL / "scripts" / "check_workflow_docs.py"


BRIEF = """# First

Status: {status}
Feature ID: B-0001

## Goal

Give the user a result.

## Stories and acceptance

### S1: First story

Story: A user acts and sees the result.

Acceptance:

- The user sees the result.

## Scope

The first result.

## Non-goals

The second result.

## Related records

- [Job reservation](../../context.md#job-reservation).
"""


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.put(
            ".workflow/backlog.md",
            "# Backlog\n\n## B-0001: First\n\n"
            "- Feature Brief: [First](features/B-0001/brief.md).\n",
        )
        self.put(
            ".workflow/context.md",
            "# Context\n\n## Job reservation\n\nA saved resource.\n",
        )
        self.put(".workflow/features/B-0001/brief.md", BRIEF.format(status="Ready"))

    def tearDown(self):
        self.temporary.cleanup()

    def put(self, name, content):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def run_check(self):
        return subprocess.run(
            [sys.executable, COMMAND, self.root],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_valid_ready_brief(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_misplaced_briefs_report_fb017_without_crashing(self):
        canonical = self.root / ".workflow/features/B-0001/brief.md"
        canonical.unlink()
        self.put(".workflow/backlog.md", "# Backlog\n")
        for name in (
            ".workflow/brief.md",
            ".workflow/features/brief.md",
            ".workflow/features/not-an-id/brief.md",
        ):
            with self.subTest(name=name):
                self.put(name, BRIEF.format(status="Ready"))
                result = self.run_check()
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(f"FB017 {name}:1", result.stdout)
                self.assertEqual(result.stderr, "")
                (self.root / name).unlink()

    def test_bundle_contains_current_validator(self):
        source = (SKILL / "scripts" / "validate.py").read_bytes()
        with zipfile.ZipFile(SKILL / "dist" / "check_workflow_docs.pyz") as bundle:
            self.assertEqual(bundle.read("__main__.py"), source)

    def test_draft_omissions_warn_and_ready_omissions_fail(self):
        incomplete = """# First

Status: {status}
Feature ID: B-0001

## Goal

## Stories and acceptance

### S1: One

### S3: Three

Story: A user acts.

Acceptance:

## Scope

## Non-goals
"""
        for status, result_code in (("Draft", 0), ("Ready", 1)):
            with self.subTest(status=status):
                self.put(
                    ".workflow/features/B-0001/brief.md",
                    incomplete.format(status=status),
                )
                result = self.run_check()
                self.assertEqual(result.returncode, result_code, result.stdout)
                for code in ("FB005", "FB007", "FB008", "FB009", "FB010"):
                    self.assertIn(code, result.stdout)
                self.assertIn(
                    "FB005 warning" if status == "Draft" else "FB005 .workflow",
                    result.stdout,
                )

    def test_draft_structure_and_anchor_fail(self):
        source = BRIEF.format(status="Draft")
        source = source.replace("B-0001", "B-0002")
        source = source.replace(
            "## Stories and acceptance",
            "## Goal\n\nAnother goal.\n\n## Stories and acceptance",
        )
        source = source.replace(
            "## Scope",
            "### S1: Duplicate\n\nStory: A second story.\n\n"
            "Acceptance:\n\n- A second result.\n\n## Scope",
        )
        source = source.replace("job-reservation", "job-reservaton")
        self.put(".workflow/features/B-0001/brief.md", source)
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        for code in ("FB003", "FB004", "FB006", "LINK002"):
            self.assertIn(code, result.stdout)

    def test_backlink_uses_targets_independent_of_labels(self):
        for line in (
            "- Brief: [First](features/B-0001/brief.md).",
            "The [first brief](features/B-0001/brief.md) defines this work.",
            "- Plan: [First][brief].\n\n[brief]: features/B-0001/brief.md",
            "- Source: [First](./features/B-0001/brief.md).",
        ):
            with self.subTest(line=line):
                self.put(".workflow/backlog.md", f"# Backlog\n\n## B-0001: First\n\n{line}\n")
                result = self.run_check()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_backlink_occurs_exactly_once(self):
        self.put(
            ".workflow/backlog.md",
            "# Backlog\n\n## B-0001: First\n\n"
            "- [First](features/B-0001/brief.md).\n"
            "- [Again](./features/B-0001/brief.md).\n",
        )
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("FB013", result.stdout)
        self.assertIn("more than once", result.stdout)

    def test_related_brief_link_is_not_an_own_backlink(self):
        first = BRIEF.format(status="Ready")
        self.put(
            ".workflow/features/B-0002/brief.md",
            first.replace("B-0001", "B-0002"),
        )
        self.put(
            ".workflow/backlog.md",
            "# Backlog\n\n## B-0001: First\n\n"
            "- [First](features/B-0001/brief.md).\n\n"
            "## B-0002: Second\n\n"
            "- Relationships: [First](features/B-0001/brief.md).\n",
        )
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("Backlog item B-0002 has no link", result.stdout)

    def test_subheadings_outside_stories_are_allowed(self):
        source = BRIEF.format(status="Ready")
        source = source.replace(
            "Give the user a result.",
            "Give the user a result.\n\n### Context\n\nThe user needs this result.",
        )
        source = source.replace(
            "The user sees the result.\n\n## Scope",
            "The user sees the result.\n\n#### Failure case\n\n"
            "A failure gives a reason.\n\n## Scope",
        )
        self.put(".workflow/features/B-0001/brief.md", source)
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_word_limit_and_heading_lint(self):
        self.put(".workflow/direction.md", "word " * 4001)
        self.put(".workflow/extra.md", "# Root\n\n### Skipped level\n\nText.\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("SIZE001", result.stdout)
        self.assertIn("MD001", result.stdout)

    def test_installed_copy_needs_no_package_install(self):
        installed = self.root / "installed-skill"
        shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns("node_modules"))
        result = subprocess.run(
            [
                sys.executable,
                installed / "scripts" / "check_workflow_docs.py",
                self.root,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
