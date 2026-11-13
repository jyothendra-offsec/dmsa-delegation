import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    return subprocess.run([sys.executable, "main.py", *args],
                          cwd=ROOT, capture_output=True, text=True, check=False)


class CliTests(unittest.TestCase):
    def test_example(self):
        result = run(*["example.csv"])
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual([x['principal'] for x in data], ['LAB Helpdesk'])

    def test_invalid_input(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "bad.csv"
            source.write_text("principal\nHelpdesk\n", encoding="utf-8")
            result = run(source, *[])
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)
