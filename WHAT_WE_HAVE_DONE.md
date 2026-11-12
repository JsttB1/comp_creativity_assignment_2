# What we have done

Status: 12 November 2026. Project: **Small Weather**, for Bad Poets Society, Assignment 2.

The poem generator, logbook, three illustrated poems and both ZIP deliverables are prepared. The assignment report remains unwritten at your request. See [what is left](WHAT_IS_LEFT.md) for the remaining requirements.

## 1. Chosen and documented the approach

- Built a Python grammar-based generator with three themes: rainy city, misty harbour and frosted garden.
- Defined a style: eight lines of free verse, arranged in four couplets, with sensory details, an emotional turn and a recurring object.
- Documented the inspiring set, initial idea, implementation decisions, limitations and AI assistance in [LOGBOOK.md](LOGBOOK.md).
- Read and referenced Sandburg's *Fog*, Dickinson's *Beclouded*, and Teasdale's *There Will Come Soft Rains*. These inform the design; the generator does not load or train on their texts.

## 2. Implemented the generator

- [poet.py](poet.py) runs offline with Python 3.10+ and the standard library.
- [data/grammar.json](data/grammar.json) contains the original, AI-assisted phrase banks and templates.
- Supports theme, seed, poem count, candidate budget, text/JSON output and an alternative grammar file.
- Stops each candidate at eight lines and each search after a bounded number of attempts: 48 by default, at most 1,000.
- Checks line length, repeated lines, unresolved placeholders and recurrence of the selected object.
- Selects a valid candidate using a simple heuristic for line length, repetition and alliteration. This score is not a measure of creativity.
- Saves seeds, grammar hashes, generator version and candidate-selection metadata for reproducibility.

Run the three selected poems again:

```sh
python3 poet.py --theme all --count 3 --seed 42
```

## 3. Generated and preserved three poems

| Poem | Theme | Seed | Winning candidate out of 48 |
| --- | --- | --- | --- |
| Rain / ticket | Rain | 42 | 28 |
| A place for sea mist | Tide | 43 | 18 |
| Frost / gate | Frost | 44 | 23 |

The complete texts and metadata are in [poems/selected.json](poems/selected.json). Individual and combined plain-text copies are in [presentation/texts](presentation/texts). The saved poems were not manually rewritten after generation.

## 4. Created the generative AI presentation

- Generated one illustration for each poem using the built-in image generation tool.
- Saved the three original PNGs in [presentation/images](presentation/images), exact prompts in [presentation/prompts](presentation/prompts), and file hashes/tool details in [presentation/provenance.json](presentation/provenance.json).
- Used the full poem in each prompt and a shared visual style across the collection.
- Typeset a three-page [poetry anthology](output/pdf/Small_Weather_Anthology.pdf), with the complete poem text kept selectable and separate from its illustration.
- Documented the distinct roles of Codex assistance, the runtime grammar generator, the image tool and PDF layout. The anthology is the presentation deliverable, not the assignment report.

## 5. Tested and reviewed the work

- All six unit tests passed under Python 3.12.10 and 3.15.2, including structural checks across 150 theme/seed combinations.
- Audited 600 outputs: 100 seeds per theme with candidate budgets of 1 and 48. All passed the mechanical rules, and every 100-poem condition had 100 distinct poem bodies. Results are in [evaluation/metrics.json](evaluation/metrics.json).
- Recorded that selection improved its own score while reducing line variety. No human reader study has been performed.
- Confirmed that the selected poems reproduce exactly, the PDF contains every poem line, and the recorded image/prompt hashes match.
- Rendered and visually inspected all three PDF pages; corrected a typography-spacing issue.
- Checked ZIP integrity, ran the extracted generator with site-packages disabled, and rebuilt a byte-identical anthology from the extracted source using the optional presentation dependencies.

## 6. Prepared the deliverables and instructions

| Item | Location | Status |
| --- | --- | --- |
| Source code, data, documentation and assets ZIP | [Small_Weather_Source.zip](output/zips/Small_Weather_Source.zip) | Prepared |
| Three illustrated poems, full texts, prompts and provenance ZIP | [Small_Weather_Presentation.zip](output/zips/Small_Weather_Presentation.zip) | Prepared |
| Poetry anthology preview | [Small_Weather_Anthology.pdf](output/pdf/Small_Weather_Anthology.pdf) | Prepared and reviewed |
| Setup and usage instructions | [README.md](README.md) | Written |
| Development record and inspiring set | [LOGBOOK.md](LOGBOOK.md) | Written |
| Assignment report using the required template | Not created | Deferred at your request |

Rebuild instructions and verification commands are in the README. The source ZIP includes the saved illustration assets so the optional anthology builder is self-contained.
