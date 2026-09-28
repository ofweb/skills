import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1] / "concise-prose"
SPEC = importlib.util.spec_from_file_location("context_glossary", SKILL / "context_glossary.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ContextGlossaryTests(unittest.TestCase):
    def test_project_glossary_adds_domain_terms_without_meanings(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "ste-glossary.json"
            project.write_text(json.dumps({
                "technical_nouns": ["redstone", {"word": "Nautilus", "inflections": ["Nautiluses"]}],
                "technical_verbs": ["attune"],
            }))
            glossary = MODULE.combined_glossary(SKILL / "shared-terms.json", project_path=project)
            nouns = {entry["word"]: entry for entry in glossary["technical_nouns"]}
            verbs = {entry["word"] for entry in glossary["technical_verbs"]}
            self.assertIn("file", nouns)
            self.assertNotIn("approved_meaning", nouns["redstone"])
            self.assertEqual(nouns["Nautilus"]["inflections"], ["Nautiluses"])
            self.assertIn("attune", verbs)

    def test_project_glossary_and_context_cannot_repeat_terms_or_forms(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project = root / "ste-glossary.json"
            context = root / "context.md"
            project.write_text(json.dumps({"technical_nouns": ["Signal"]}))
            context.write_text("# Context\n\n## Signal\n- Meaning: A Signal is an event.\n- STE class: Technical name\n")
            with self.assertRaisesRegex(ValueError, "conflicts"):
                MODULE.combined_glossary(SKILL / "shared-terms.json", context, project)
            project.write_text(json.dumps({"technical_nouns": [{"word": "redstone", "inflections": ["file"]}]}))
            with self.assertRaisesRegex(ValueError, "conflicts"):
                MODULE.combined_glossary(SKILL / "shared-terms.json", project_path=project)
            project.write_text(json.dumps({"technical_nouns": ["redstone", "Redstone"]}))
            with self.assertRaisesRegex(ValueError, "conflicts"):
                MODULE.combined_glossary(SKILL / "shared-terms.json", project_path=project)

    def test_project_glossary_rejects_meanings_and_bad_forms(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "ste-glossary.json"
            project.write_text(json.dumps({"technical_nouns": [{"word": "redstone", "approved_meaning": "A block."}]}))
            with self.assertRaisesRegex(ValueError, "Invalid project glossary entry"):
                MODULE.combined_glossary(SKILL / "shared-terms.json", project_path=project)
            project.write_text(json.dumps({"technical_nouns": [{"word": "redstone", "inflections": "redstones"}]}))
            with self.assertRaisesRegex(ValueError, "forms"):
                MODULE.combined_glossary(SKILL / "shared-terms.json", project_path=project)

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
