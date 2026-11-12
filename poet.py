#!/usr/bin/env python3
"""Small Weather: a finite, seeded grammar with an explicitly limited critic.

The runtime uses Python's standard library only. It neither calls an LLM nor
loads the inspiring poems. Read LOGBOOK.md for the AI-assisted development role.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import random
import re
import secrets
import string
import sys
from typing import Any

ROOT = Path(__file__).resolve().parent
DEFAULT_GRAMMAR = ROOT / "data" / "grammar.json"
GENERATOR_VERSION = "1.0"
STOPWORDS = set("a an the of in on at to for and but its is it i my our with as by all this that one has have still even now".split())


@dataclass(frozen=True)
class Poem:
    title: str
    lines: tuple[str, ...]
    theme: str
    seed: int
    motif: str
    score: float
    candidate_index: int
    candidates_tried: int
    grammar_sha256: str
    generator_version: str = GENERATOR_VERSION

    @property
    def text(self) -> str:
        stanzas = ["\n".join(self.lines[i:i + 2]) for i in range(0, 8, 2)]
        return self.title + "\n\n" + "\n\n".join(stanzas) + "\n"

    def to_dict(self) -> dict[str, Any]:
        return {**asdict(self), "text": self.text}


def words(text: str) -> list[str]:
    return re.findall(r"[a-z]+(?:[-'][a-z]+)*", text.lower())


def sentence(text: str) -> str:
    """Capitalise only the initial character, preserving the rest of the text."""
    return text[0].upper() + text[1:]


def load_grammar(path: Path = DEFAULT_GRAMMAR) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Grammar must be a JSON object.")

    def nonempty_strings(value: Any, name: str) -> None:
        if not isinstance(value, list) or not value or any(not isinstance(x, str) or not x.strip() for x in value):
            raise ValueError(f"{name} must be a nonempty list of strings.")

    common = data.get("common")
    themes = data.get("themes")
    templates = data.get("templates")
    if not isinstance(common, dict) or not isinstance(themes, dict) or not themes:
        raise ValueError("Grammar needs common banks and at least one theme.")
    for name in ("memory", "action", "turn", "return_action", "title"):
        nonempty_strings(common.get(name), f"common.{name}")
    if not isinstance(templates, list) or len(templates) != 8:
        raise ValueError("Grammar must contain exactly eight line-template banks.")
    allowed = set("place weather weather_action adjective motif action memory sound detail turn counterpoint return_action ending".split())
    for index, bank in enumerate(templates):
        nonempty_strings(bank, f"templates[{index}]")
    # Disallow attributes, indexing, conversions and formatting directives.
    for pattern in [item for bank in templates for item in bank] + common["title"]:
        for _, field, spec, conversion in string.Formatter().parse(pattern):
            if field is not None and (field not in allowed or spec or conversion):
                raise ValueError(f"Unsupported template field: {field!r}")
    for name, theme in themes.items():
        if not isinstance(theme, dict):
            raise ValueError(f"Theme {name} must be an object.")
        if not isinstance(theme.get("weather"), str) or not theme["weather"].strip():
            raise ValueError(f"Theme {name} needs a weather phrase.")
        for key in ("places", "weather_actions", "sounds", "details", "counterpoints", "endings"):
            nonempty_strings(theme.get(key), f"{name}.{key}")
        motifs = theme.get("motifs")
        if not isinstance(motifs, list) or not motifs:
            raise ValueError(f"Theme {name} needs motifs.")
        for motif in motifs:
            if not isinstance(motif, dict) or any(not isinstance(motif.get(k), str) or not motif[k].strip() for k in ("noun", "adjective")):
                raise ValueError(f"Theme {name} needs noun/adjective motif pairs.")
    return data


def grammar_digest(grammar: dict[str, Any]) -> str:
    canonical = json.dumps(grammar, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def candidate(grammar: dict[str, Any], theme: str, rng: random.Random) -> tuple[str, tuple[str, ...], str]:
    bank = grammar["themes"][theme]
    motif = rng.choice(bank["motifs"])
    context = {
        "motif": motif["noun"], "adjective": motif["adjective"],
        "weather": bank["weather"],
        **{key: rng.choice(grammar["common"][key]) for key in ("memory", "action", "turn", "return_action")},
        **{slot: rng.choice(bank[key]) for slot, key in (
            ("place", "places"), ("weather_action", "weather_actions"),
            ("sound", "sounds"), ("detail", "details"),
            ("counterpoint", "counterpoints"), ("ending", "endings"),
        )},
    }
    lines = tuple(sentence(rng.choice(options).format_map(context)) for options in grammar["templates"])
    title = sentence(rng.choice(grammar["common"]["title"]).format_map(context))
    return title, lines, motif["noun"]


def violations(lines: tuple[str, ...], motif: str) -> list[str]:
    """Mechanical requirements, not an aesthetic or semantic judgement."""
    failures = []
    if len(lines) != 8:
        failures.append("expected eight lines")
    if len(set(lines)) != len(lines):
        failures.append("duplicate lines")
    if any(not 4 <= len(words(line)) <= 14 for line in lines):
        failures.append("a line falls outside 4-14 words")
    if any("{" in line or "}" in line or "\n" in line for line in lines):
        failures.append("unresolved placeholder or embedded line break")
    if len(lines) == 8 and any(motif not in line.lower() for line in (lines[1], lines[6])):
        failures.append("missing recurring motif")
    return failures


def craft_score(lines: tuple[str, ...], motif: str) -> float:
    """An intentionally modest heuristic; never label this 'creativity'.

    Prefer seven-word lines, varied vocabulary outside the recurring motif,
    and a little alliteration. The weights express design preferences.
    """
    line_words = [words(line) for line in lines]
    excluded = STOPWORDS | set(words(motif))
    content = [[word for word in line if word not in excluded] for line in line_words]
    counts = Counter(word for line in content for word in line)
    repetition = sum(max(0, count - 1) for count in counts.values())
    length_cost = sum(abs(len(line) - 7) for line in line_words)
    echoes = sum(any(a[0] == b[0] for a, b in zip(line, line[1:])) for line in content)
    return round(100 - 1.25 * length_cost - 3 * repetition + 0.75 * min(echoes, 4), 2)


def generate(theme: str = "rain", seed: int = 42, candidates: int = 48,
             grammar: dict[str, Any] | None = None) -> Poem:
    if not 1 <= candidates <= 1000:
        raise ValueError("Candidates must be between 1 and 1000.")
    grammar = load_grammar() if grammar is None else grammar
    if theme not in grammar["themes"]:
        raise ValueError(f"Unknown theme {theme!r}; choose from {', '.join(grammar['themes'])}.")
    rng = random.Random(seed)
    best = None
    # Finite search: always stop after this many attempts, including failures.
    for index in range(candidates):
        title, lines, motif = candidate(grammar, theme, rng)
        if violations(lines, motif):
            continue
        score = craft_score(lines, motif)
        if best is None or score > best[0]:
            best = (score, index + 1, title, lines, motif)
    if best is None:
        raise ValueError(f"No valid poem among {candidates} candidates; check the grammar.")
    score, index, title, lines, motif = best
    return Poem(title, lines, theme, seed, motif, score, index, candidates, grammar_digest(grammar))


def bounded_int(low: int, high: int):
    def parse(value: str) -> int:
        try:
            number = int(value)
        except ValueError as error:
            raise argparse.ArgumentTypeError("Expected an integer.") from error
        if not low <= number <= high:
            raise argparse.ArgumentTypeError(f"Expected a number from {low} to {high}.")
        return number
    return parse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--theme", default="rain", help="Theme name or 'all' to cycle through themes.")
    parser.add_argument("--seed", type=int, help="Integer seed; omitted seeds are random and printed to stderr.")
    parser.add_argument("--count", type=bounded_int(1, 100), default=1, help="Poems to generate (1-100).")
    parser.add_argument("--candidates", type=bounded_int(1, 1000), default=48, help="Bounded candidate budget per poem.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--output", type=Path, help="Save to a new file instead of stdout.")
    parser.add_argument("--grammar", type=Path, default=DEFAULT_GRAMMAR)
    args = parser.parse_args(argv)
    try:
        grammar = load_grammar(args.grammar)
        if args.theme != "all" and args.theme not in grammar["themes"]:
            raise ValueError(f"Unknown theme {args.theme!r}; choose {', '.join(grammar['themes'])}, or all.")
        seed = args.seed if args.seed is not None else secrets.randbits(63)
        if args.seed is None:
            print(f"Seed: {seed}", file=sys.stderr)
        themes = list(grammar["themes"]) if args.theme == "all" else [args.theme]
        poems = [generate(themes[i % len(themes)], seed + i, args.candidates, grammar) for i in range(args.count)]
        if args.format == "json":
            output = json.dumps([poem.to_dict() for poem in poems], indent=2, ensure_ascii=False) + "\n"
        else:
            output = "\n---\n\n".join(poem.text for poem in poems)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x", encoding="utf-8") as handle:
                handle.write(output)
        else:
            print(output, end="")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
