#!/usr/bin/env python3
"""Create the two requested ZIP archives from an explicit file allowlist."""

import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "output" / "zips"


def zip_files(destination, entries):
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        for path, name in entries:
            archive.write(path, name)
    with ZipFile(destination) as archive:
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"Corrupt ZIP entry: {bad}")
    return {"file": destination.name, "bytes": destination.stat().st_size,
            "sha256": hashlib.sha256(destination.read_bytes()).hexdigest()}


def main():
    pdf = ROOT / "output" / "pdf" / "Small_Weather_Anthology.pdf"
    if not pdf.exists():
        raise SystemExit("Build the poetry anthology before packaging.")
    source_paths = [ROOT / name for name in (
        "README.md", "LOGBOOK.md", "poet.py", "requirements-presentation.txt", "requirements-qa.txt",
        "WHAT_WE_HAVE_DONE.md", "WHAT_IS_LEFT.md",
        "Bad_Poets_Society_Assignment_2.md",
    )]
    for folder in ("data", "tests", "scripts", "poems", "evaluation", "presentation"):
        source_paths.extend(path for path in sorted((ROOT / folder).rglob("*"))
                            if path.is_file() and "__pycache__" not in path.parts
                            and path.name != ".DS_Store")
    source = [(path, str(Path("small_weather_source") / path.relative_to(ROOT))) for path in source_paths]
    presentation = [(path, str(Path("small_weather_presentation") / path.relative_to(ROOT / "presentation")))
                    for path in sorted((ROOT / "presentation").rglob("*"))
                    if path.is_file() and path.name != ".DS_Store"]
    presentation.extend([
        (pdf, "small_weather_presentation/Small_Weather_Anthology.pdf"),
        (ROOT / "poems" / "selected.json", "small_weather_presentation/selected.json"),
    ])
    DESTINATION.mkdir(parents=True, exist_ok=True)
    results = [
        zip_files(DESTINATION / "Small_Weather_Source.zip", source),
        zip_files(DESTINATION / "Small_Weather_Presentation.zip", presentation),
    ]
    (DESTINATION / "checksums.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
