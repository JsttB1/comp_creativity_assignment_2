"""Check generation contracts, reproducibility, and bounded failure."""

import copy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from poet import generate, load_grammar, violations


class GeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grammar = load_grammar()

    def test_reproducibility(self):
        self.assertEqual(generate(seed=42), generate(seed=42))

    def test_contract_across_themes_and_seeds(self):
        for theme in self.grammar["themes"]:
            for seed in range(50):
                with self.subTest(theme=theme, seed=seed):
                    poem = generate(theme, seed, grammar=self.grammar)
                    self.assertEqual(violations(poem.lines, poem.motif), [])
                    self.assertEqual(len(poem.text.strip().split("\n\n")), 5)
                    self.assertTrue(1 <= poem.candidate_index <= poem.candidates_tried == 48)

    def test_seed_changes_output(self):
        texts = {generate(seed=seed, grammar=self.grammar).text for seed in range(20)}
        self.assertEqual(len(texts), 20)

    def test_bounded_failure(self):
        grammar = copy.deepcopy(self.grammar)
        grammar["templates"][0] = ["Too short."]
        with self.assertRaisesRegex(ValueError, "No valid poem among 3 candidates"):
            generate(candidates=3, grammar=grammar)

    def test_bad_arguments(self):
        for value in (0, -1, 1001):
            with self.assertRaises(ValueError):
                generate(candidates=value)
        with self.assertRaisesRegex(ValueError, "Unknown theme"):
            generate(theme="missing")

    def test_cli_runs_outside_project_and_protects_existing_files(self):
        script = Path(__file__).resolve().parents[1] / "poet.py"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "poem.txt"
            command = [sys.executable, str(script), "--seed", "42", "--output", str(path)]
            first = subprocess.run(command, cwd=directory, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            original = path.read_bytes()
            second = subprocess.run(command, cwd=directory, capture_output=True, text=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
