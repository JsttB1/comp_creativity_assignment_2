#!/usr/bin/env python3
"""Reproduce the two supplementary statistics cited in the report.

1. Validator failure rate over 20,000 raw candidates per theme (seeded).
2. How often each common phrase wins under 1 vs 48 candidates (seeds 0-99,
   all themes), compared with the uniform expectation.
Writes evaluation/selection_bias.json. Standard library only.
"""

from collections import Counter
import json
import math
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import poet  # noqa: E402


def main():
    grammar = poet.load_grammar()
    common = grammar["common"]
    templates = math.prod(len(bank) for bank in grammar["templates"])
    result = {"grammar_sha256": poet.grammar_digest(grammar), "space": {}, "validator": {}, "phrase_frequency": {}}
    for theme, bank in grammar["themes"].items():
        size = len(bank["motifs"]) * templates
        size *= math.prod(len(common[k]) for k in ("memory", "action", "turn", "return_action"))
        size *= math.prod(len(bank[k]) for k in ("places", "weather_actions", "sounds", "details", "counterpoints", "endings"))
        result["space"][theme] = size
        rng, failures, samples = random.Random(1), 0, 20000
        for _ in range(samples):
            _, lines, motif = poet.candidate(grammar, theme, rng)
            failures += bool(poet.violations(lines, motif))
        result["validator"][theme] = {"samples": samples, "failures": failures}
    for budget in (1, 48):
        memory, turn, ret = Counter(), Counter(), Counter()
        for theme in grammar["themes"]:
            for seed in range(100):
                poem = poet.generate(theme, seed, budget, grammar)
                memory[next(m for m in common["memory"] if m in poem.lines[1])] += 1
                turn[poem.lines[4]] += 1
                ret[next(r for r in common["return_action"] if r in poem.lines[6])] += 1
        result["phrase_frequency"][str(budget)] = {
            "poems": 300,
            "uniform_expectation": {"memory": 300 / len(common["memory"]), "turn": 300 / len(common["turn"]),
                                    "return_action": 300 / len(common["return_action"])},
            "memory": dict(memory.most_common()), "turn": dict(turn.most_common()),
            "return_action": dict(ret.most_common()),
        }
    out = ROOT / "evaluation" / "selection_bias.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
