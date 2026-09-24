import importlib.util
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1] / "concise-prose"
SPEC = importlib.util.spec_from_file_location("context_glossary", SKILL / "context_glossary.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ContextGlossaryTests(unittest.TestCase):
    def test_approved_context_entries_extend_shared_terms(self):
        with tempfile.TemporaryDirectory() as temporary:
            context = Path(temporary) / "context.md"
            context.write_text(
                "# Context\n\n"
                "## Signal\n- Meaning: A project event.\n"
                "- STE class: Technical name\n- Forms: Signals\n\n"
                "## Escrow\n- Meaning: To hold an amount.\n"
                "- STE class: Technical verb\n- Forms: Escrows, Escrowed\n"
            )
            glossary = MODULE.combined_glossary(SKILL / "shared-terms.json", context)
            nouns = {entry["word"] for entry in glossary["technical_nouns"]}
            verbs = {entry["word"] for entry in glossary["technical_verbs"]}
            self.assertIn("file", nouns)
            self.assertIn("Signal", nouns)
            self.assertIn("Escrow", verbs)

    def test_context_cannot_override_shared_or_repeat_a_term(self):
        with tempfile.TemporaryDirectory() as temporary:
            context = Path(temporary) / "context.md"
            context.write_text(
                "# Context\n\n## file\n- Meaning: Another meaning.\n"
                "- STE class: Technical name\n"
            )
            with self.assertRaisesRegex(ValueError, "conflicts"):
                MODULE.combined_glossary(SKILL / "shared-terms.json", context)

    def test_candidate_status_cannot_approve_vocabulary(self):
        with tempfile.TemporaryDirectory() as temporary:
            context = Path(temporary) / "context.md"
            context.write_text(
                "# Context\n\n## Signal\n- Status: Proposed\n"
                "- Meaning: A possible project event.\n"
                "- STE class: Technical name\n"
            )
            with self.assertRaisesRegex(ValueError, "not agreed"):
                MODULE.combined_glossary(SKILL / "shared-terms.json", context)


if __name__ == "__main__":
    unittest.main()
