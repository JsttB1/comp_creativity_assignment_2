#!/usr/bin/env python3
"""Verify exact poem reproduction, asset hashes, PDF text and page bounds."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

import pymupdf
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from poet import generate


def verify(render_dir=None):
    poems = json.loads((ROOT / "poems" / "selected.json").read_text(encoding="utf-8"))
    records = json.loads((ROOT / "presentation" / "provenance.json").read_text(encoding="utf-8"))
    path = ROOT / "output" / "pdf" / "Small_Weather_Anthology.pdf"
    pdf = PdfReader(path)
    assert len(pdf.pages) == len(poems) == len(records) == 3, "Expected three presentation pages."
    for poem, record, page in zip(poems, records, pdf.pages):
        reproduced = generate(poem["theme"], poem["seed"], poem["candidates_tried"])
        assert json.loads(json.dumps(reproduced.to_dict())) == poem, "Saved output does not reproduce."
        text = page.extract_text()
        assert poem["title"] in text
        for line in poem["lines"]:
            assert line in text, f"Missing PDF line: {line}"
        text_file = ROOT / "presentation" / record["poem_file"]
        assert text_file.read_text(encoding="utf-8") == poem["text"]
        assert hashlib.sha256(text_file.read_bytes()).hexdigest() == record["poem_text_sha256"]
        for field, hash_field in (("image_file", "image_sha256"), ("prompt_file", "prompt_sha256")):
            asset = ROOT / "presentation" / record[field]
            assert hashlib.sha256(asset.read_bytes()).hexdigest() == record[hash_field]
        assert poem["text"] in (ROOT / "presentation" / record["prompt_file"]).read_text(encoding="utf-8")
    with pymupdf.open(path) as document:
        for index, page in enumerate(document, 1):
            for block in page.get_text("dict")["blocks"]:
                if block["type"] == 0:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            x0, y0, x1, y1 = span["bbox"]
                            assert 0 <= x0 < x1 <= page.rect.width, span
                            assert 0 <= y0 < y1 <= page.rect.height, span
            if render_dir:
                render_dir.mkdir(parents=True, exist_ok=True)
                page.get_pixmap(matrix=pymupdf.Matrix(1.4, 1.4), alpha=False).save(render_dir / f"anthology-{index}.png")
    print("PASS: three poems reproduced exactly; all PDF lines present; asset hashes match; text inside page bounds.")
    if render_dir:
        print(f"Rendered {len(poems)} pages to {render_dir}; inspect these images for visual quality.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render-dir", type=Path)
    args = parser.parse_args()
    verify(args.render_dir)
