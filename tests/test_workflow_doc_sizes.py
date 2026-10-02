import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1] / "workflow-document-check"
SCRIPT = SKILL / "scripts" / "check_workflow_docs.py"


class WorkflowDocumentSizeTests(unittest.TestCase):
    def run_checker(self, root):
        return subprocess.run(
            [sys.executable, SCRIPT, root],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_all_existing_document_limits(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflow = root / ".workflow"
            documents = {
                "direction.md": (4000, "Direction"),
                "direction/topic.md": (2000, "Direction topic"),
                "backlog.md": (1800, "Backlog"),
                "context.md": (5000, "Context"),
                "decisions/pdr/0001-choice.md": (500, "PDR"),
                "decisions/adr/0001-choice.md": (700, "ADR"),
                "features/B-0001/acceptance-2026-09-24-abcdef0.md": (800, "Acceptance Report"),
            }
            for name, (limit, _) in documents.items():
                path = workflow / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("word " * (limit + 1))
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 1, result.stderr)
            for _, label in documents.values():
                self.assertIn(label, result.stdout)

    def test_context_document_limit_boundary(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflow = root / ".workflow"
            workflow.mkdir()
            context = workflow / "context.md"
            source = "# Context\n\n" + "\n\n".join(
                f"## Term{index}\n\n- Meaning: " + "word " * 46
                for index in range(100)
            )
            self.assertEqual(len(source.split()), 5002)
            context.write_text(source.replace("word word ", "", 1))
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            context.write_text(context.read_text() + "extra ")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("Context", result.stdout)
            self.assertIn("5001", result.stdout)
            self.assertNotIn("Context entry", result.stdout)

    def test_record_limits(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflow = root / ".workflow"
            workflow.mkdir()
            (workflow / "backlog.md").write_text(
                "# Backlog\n\n## B-0001: Item\n\n" + "word " * 78
            )
            (workflow / "context.md").write_text(
                "# Context\n\n## Term\n\n" + "word " * 79
            )
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("Backlog item", result.stdout)
            self.assertIn("Context entry", result.stdout)

    def test_compatibility_command_works_from_installed_skill(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            installed = root / "installed-checker"
            project = root / "project"
            shutil.copytree(
                SKILL,
                installed,
                ignore=shutil.ignore_patterns("node_modules", "package-lock.json"),
            )
            (project / ".workflow").mkdir(parents=True)
            (project / ".workflow" / "direction.md").write_text("# Direction\n")
            result = subprocess.run(
                [sys.executable, installed / "scripts" / "check_workflow_docs.py", project],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("passed validation", result.stdout)

    def test_draft_warning_and_ready_error_exit_codes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflow = root / ".workflow"
            brief = workflow / "features" / "B-0001" / "brief.md"
            brief.parent.mkdir(parents=True)
            (workflow / "backlog.md").write_text(
                "# Backlog\n\n## B-0001: First\n\n"
                "- Feature Brief: [First](features/B-0001/brief.md).\n"
            )
            source = "# First\n\nStatus: {}\nFeature ID: B-0001\n\n## Goal\n"
            brief.write_text(source.format("Draft"))
            draft = self.run_checker(root)
            self.assertEqual(draft.returncode, 0, draft.stderr)
            self.assertIn("FB005 warning", draft.stdout)

            brief.write_text(source.format("Ready"))
            ready = self.run_checker(root)
            self.assertEqual(ready.returncode, 1, ready.stderr)
            self.assertIn("FB005 .workflow/features/B-0001/brief.md:6", ready.stdout)


if __name__ == "__main__":
    unittest.main()
