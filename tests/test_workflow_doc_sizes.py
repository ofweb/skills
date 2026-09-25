import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1] / "workflow-document-check"
SCRIPT = SKILL / "scripts" / "check_workflow_docs.py"
SPEC = importlib.util.spec_from_file_location("check_workflow_docs", SCRIPT)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class WorkflowDocumentSizeTests(unittest.TestCase):
    def test_single_document_hard_limits(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflow = root / ".workflow"
            pdr = workflow / "decisions" / "pdr" / "0001-choice.md"
            adr = workflow / "decisions" / "adr" / "0001-choice.md"
            pdr.parent.mkdir(parents=True)
            adr.parent.mkdir(parents=True)
            (workflow / "direction.md").write_text("word " * 4000)
            pdr.write_text("word " * 500)
            adr.write_text("word " * 700)
            self.assertEqual(CHECKER.check(root), [])

            (workflow / "direction.md").write_text("word " * 4001)
            pdr.write_text("word " * 501)
            adr.write_text("word " * 701)
            findings = CHECKER.check(root)
            self.assertEqual(len(findings), 3)
            self.assertTrue(any("Direction" in item for item in findings))
            self.assertTrue(any("PDR" in item for item in findings))
            self.assertTrue(any("ADR" in item for item in findings))

    def test_direction_topic_limits_are_independent(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflow = root / ".workflow"
            topics = workflow / "direction"
            topics.mkdir(parents=True)
            (workflow / "direction.md").write_text("word " * 4000)
            first = topics / "runtime.md"
            second = topics / "device.md"
            first.write_text("word " * 2000)
            second.write_text("word " * 2000)
            self.assertEqual(CHECKER.check(root), [])

            second.write_text("word " * 2001)
            findings = CHECKER.check(root)
            self.assertEqual(len(findings), 1)
            self.assertIn("Direction topic", findings[0])

    def test_installed_checker_enforces_feature_brief_limit(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            installed = root / "installed-checker"
            project = root / "project"
            brief = project / ".workflow" / "features" / "B-0001" / "brief.md"
            second = project / ".workflow" / "features" / "B-0002" / "brief.md"
            shutil.copytree(SKILL, installed)
            brief.parent.mkdir(parents=True)
            second.parent.mkdir(parents=True)
            brief.write_text("word " * 1000)
            second.write_text("word " * 1000)
            command = [sys.executable, installed / "scripts" / "check_workflow_docs.py", project]
            passed = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(passed.returncode, 0, passed.stdout)

            brief.write_text("word " * 1001)
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("Feature Brief", result.stdout)

    def test_record_limit_and_whole_file_limit(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflow = root / ".workflow"
            workflow.mkdir()
            (workflow / "backlog.md").write_text("# Backlog\n\n## B-0001: Item\n" + "word " * 78)
            (workflow / "context.md").write_text(
                "# Context\n\n" + "\n".join(f"## Term {n}\n" + "word " * 77 for n in range(20))
            )
            findings = CHECKER.check(root)
            self.assertTrue(any("Backlog item" in item for item in findings))
            self.assertTrue(any("Context; hard limit 1500" in item for item in findings))
            self.assertFalse(any("Context entry" in item for item in findings))

    def test_acceptance_reports_have_independent_limits(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            feature = root / ".workflow" / "features" / "B-0001"
            feature.mkdir(parents=True)
            first = feature / "acceptance-2026-09-24-abcdef0.md"
            second = feature / "acceptance-2026-09-25-abcdef1.md"
            first.write_text("word " * 800)
            second.write_text("word " * 800)
            self.assertEqual(CHECKER.check(root), [])

            second.write_text("word " * 801)
            findings = CHECKER.check(root)
            self.assertEqual(len(findings), 1)
            self.assertIn("Acceptance Report", findings[0])


if __name__ == "__main__":
    unittest.main()
