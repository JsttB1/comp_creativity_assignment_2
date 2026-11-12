#!/usr/bin/env python3
"""Reproducible mechanical audit; this does not measure artistic creativity."""

from collections import Counter
import json
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from poet import generate, load_grammar, violations, words


def evaluate():
    grammar = load_grammar()
    results = {
        "design": "100 seeds (0-99) per theme, candidate budgets 1 and 48; no human raters",
        "limitations": "Heuristic scores and distinct strings are not measures of creativity or literary quality.",
        "grammar_sha256": generate(grammar=grammar).grammar_sha256,
        "conditions": [],
    }
    for theme in grammar["themes"]:
        for budget in (1, 48):
            poems = [generate(theme, seed, budget, grammar) for seed in range(100)]
            line_counts = Counter(line for poem in poems for line in poem.lines)
            scores = [poem.score for poem in poems]
            results["conditions"].append({
                "theme": theme,
                "candidates": budget,
                "sample_size": len(poems),
                "valid_poems": sum(not violations(poem.lines, poem.motif) for poem in poems),
                "distinct_poem_bodies": len({poem.lines for poem in poems}),
                "distinct_lines": len(line_counts),
                "total_lines": len(poems) * 8,
                "mean_words_per_line": round(statistics.mean(len(words(line)) for poem in poems for line in poem.lines), 2),
                "mean_heuristic_score": round(statistics.mean(scores), 2),
                "min_heuristic_score": min(scores),
                "max_heuristic_score": max(scores),
                "most_repeated_line": line_counts.most_common(1)[0],
            })
    path = ROOT / "evaluation" / "metrics.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    evaluate()
