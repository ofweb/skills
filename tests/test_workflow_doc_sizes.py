import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_workflow_docs.py"
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
            (workflow / "direction.md").write_text("word " * 800)
            pdr.write_text("word " * 500)
            adr.write_text("word " * 700)
            self.assertEqual(CHECKER.check(root), [])

            (workflow / "direction.md").write_text("word " * 801)
            pdr.write_text("word " * 501)
            adr.write_text("word " * 701)
            findings = CHECKER.check(root)
            self.assertEqual(len(findings), 3)
            self.assertTrue(any("Direction" in item for item in findings))
            self.assertTrue(any("PDR" in item for item in findings))
            self.assertTrue(any("ADR" in item for item in findings))

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


if __name__ == "__main__":
    unittest.main()
