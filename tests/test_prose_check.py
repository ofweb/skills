from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SKILL_DIR = Path(__file__).resolve().parents[1] / "concise-prose"
REAL_VALE = shutil.which("vale")


class CommandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        tools = self.directory / "tools"
        tools.mkdir()
        (tools / "python3").symlink_to(sys.executable)
        vale = tools / "vale"
        vale.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, sys\n"
            "print(json.dumps({'args': sys.argv[1:], 'stdin': sys.stdin.read()}))\n"
            "print('vale diagnostic', file=sys.stderr)\n"
            "status = int(os.environ.get('FAKE_VALE_STATUS', '0'))\n"
            "sys.exit(1 if sys.argv[-1].endswith('bad.md') else status)\n"
        )
        vale.chmod(0o755)
        self.env = dict(os.environ, PATH=str(tools))

    def run_tool(
        self, *args: str, input_text: str | None = None, skill_dir: Path = SKILL_DIR
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(skill_dir / "prose-check"), *args],
            input=input_text,
            text=True,
            capture_output=True,
            env=self.env,
            check=False,
        )

    def test_stdin_uses_markdown_and_bundled_config_without_other_tools(self) -> None:
        source = "# Signal\n\nUse `signal`.\n"
        for args in ((), ("-",)):
            with self.subTest(args=args):
                result = self.run_tool(*args, input_text=source)
                self.assertEqual(result.returncode, 0, result.stderr)
                report = json.loads(result.stdout.splitlines()[1])
                self.assertEqual(report['stdin'], source)
                self.assertEqual(report['args'], [
                    '--config', str(SKILL_DIR / '.vale.ini'),
                    '--ext=.md', '--path=stdin.md',
                ])
                self.assertIn('vale diagnostic', result.stderr)

    def test_file_checks_continue_after_lint_and_input_failures(self) -> None:
        bad = self.directory / 'bad.md'
        good = self.directory / 'good.md'
        bad.write_text('Note that the file exists.\n')
        good.write_text('Use the file.\n')
        result = self.run_tool(str(bad), str(good))
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(f'== {good}: Vale ==', result.stdout)
        self.assertLess(result.stdout.index(str(bad)), result.stdout.index(str(good)))

        result = self.run_tool(str(self.directory / 'missing.md'), str(good))
        self.assertEqual(result.returncode, 2)
        self.assertIn('missing.md', result.stderr)
        self.assertIn(f'== {good}: Vale ==', result.stdout)

    def test_tool_failures_are_not_clean_checks(self) -> None:
        self.env['FAKE_VALE_STATUS'] = '2'
        result = self.run_tool(input_text='Use the file.\n')
        self.assertEqual(result.returncode, 2)
        (self.directory / 'tools' / 'vale').unlink()
        result = self.run_tool(input_text='Use the file.\n')
        self.assertEqual(result.returncode, 2)
        self.assertIn('missing command: vale', result.stderr)

    def test_installed_copy_uses_its_own_configuration(self) -> None:
        installed = self.directory / 'installed-prose'
        shutil.copytree(SKILL_DIR, installed)
        result = self.run_tool(input_text='Use the file.\n', skill_dir=installed)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout.splitlines()[1])
        self.assertEqual(report['args'][1], str(installed / '.vale.ini'))


@unittest.skipUnless(REAL_VALE, 'Vale is required')
class ValeTests(unittest.TestCase):
    def run_tool(self, *args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(SKILL_DIR / 'prose-check'), *args],
            input=input_text, text=True, capture_output=True, check=False,
        )

    def test_real_vale_checks_stdin_and_ignores_markdown_code(self) -> None:
        source = (
            'Use the file.\n\n'
            '`Note that the relevant file exists.`\n\n'
            '```text\nNote that the relevant file exists.\n```\n'
        )
        passed = self.run_tool(input_text=source)
        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
        failed = self.run_tool('-', input_text='Use the relevant file.\n')
        self.assertEqual(failed.returncode, 1, failed.stderr)
        self.assertIn('Empty qualifier', failed.stdout)

    def test_real_vale_keeps_mechanical_rules_and_source_locations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / 'guide.md'
            source.write_text('# Guide\n\nNote that the file exists.\n')
            result = self.run_tool(str(source))
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn('Throat-clearing', result.stdout)
            self.assertIn('3:1', result.stdout)

        for text, message in (
            ('It could be argued that the file exists.', 'Hedge'),
            ('The file exists for various reasons.', 'Non-reason'),
            ('Furthermore, the file exists.', 'Stock connective'),
            ('The code handles this gracefully.', 'Self-praise'),
            ('This function returns the file.', 'Restates the code'),
        ):
            with self.subTest(text=text):
                result = self.run_tool(input_text=text + '\n')
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(message, result.stdout)

    def test_technical_terms_and_long_sentences_need_no_glossary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            workflow = project / '.workflow'
            workflow.mkdir()
            (workflow / 'context.md').write_text('# Context\n\n## Incomplete\n')
            source = project / 'guide.md'
            source.write_text(
                'The scheduler saves a reservation for each pending task so that '
                'the worker can resume processing after a restart without losing '
                'the task identifier or its original position in the queue.\n'
            )
            result = self.run_tool(str(source))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
