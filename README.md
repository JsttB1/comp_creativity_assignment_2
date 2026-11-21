# Small Weather

A reproducible Python poem generator for **Bad Poets Society, Assignment 2**. It writes eight-line free-verse poems about a rainy city, a misty harbour or a frosted garden. Each poem introduces an ordinary object, gives it an emotional trace, and returns to it before closing.

The project includes a documented inspiring set, runnable source, three generated poems, three AI illustrations, a typeset poetry anthology, two ZIP packages and the four-page ICCC-format report (`output/pdf/Small_Weather_Report.pdf`, LaTeX source in `report/`).

Project status: [what we have done](WHAT_WE_HAVE_DONE.md) and [what is left](WHAT_IS_LEFT.md).

## Run the generator

**Requirements:** Python 3.10 or newer. No external packages, API keys, network connection or compilation are needed for poem generation. Tested with Python 3.12.10 and 3.15.2.

From the project folder:

```sh
python3 poet.py --theme rain --seed 42
python3 poet.py --theme tide --seed 123 --candidates 48
python3 poet.py --theme all --count 3 --seed 42
python3 poet.py --theme frost --count 5 --format json --output poems/new_frost_poems.json
```

On Windows, use `python` or `py` instead of `python3` if necessary. Omitting `--seed` chooses a random seed and prints it to stderr. `--theme all` cycles through rain, tide and frost; the seed increments once per poem. `--count` defaults to 1, including with `--theme all`. Files named by `--output` must not already exist, to protect previously saved poems. Run `python3 poet.py --help` for all options.

To reproduce the anthology poems, use `--theme all --count 3 --seed 42` with the default 48 candidates. The saved texts have not been manually edited. A given code version, grammar and compatible Python random implementation reproduce the poem; the seed alone does not describe later changes to the grammar.

## How it works

`data/grammar.json` contains original, AI-assisted phrase banks and eight template slots. Each candidate uses one theme and one recurring object. Its four couplets move through scene-setting, sensory detail, an emotional turn and a closing image.

The generator tries exactly 48 candidates by default. Each candidate ends after eight lines. It checks line length (4-14 words), motif recurrence, duplicate lines and unresolved placeholders. Among valid candidates, a simple critic prefers lines near seven words, limited word repetition and some alliteration. Ties choose the earliest candidate. If every candidate fails, generation exits with an error. Candidate count is bounded at 1-1,000 and poem count at 1-100.

The score is a craft heuristic, **not a creativity measurement**. There is no language model, external corpus, syllable counter or rhyme engine running inside the generator. The inspiring poems inform the design but are not read by the program.

## Read the outputs

- `output/pdf/Small_Weather_Anthology.pdf`: three illustrated poems, with selectable text.
- `poems/selected.json`: complete poems and generation metadata.
- `presentation/texts/`: individual full texts and a combined text file.
- `presentation/images/`: the three original generated PNGs.
- `presentation/prompts/`: the exact image-generation prompts, including the source poem.
- `presentation/provenance.json`: seeds, candidate indices, file hashes, tool attribution and image provenance.
- `LOGBOOK.md`: inspiring set, design decisions, observed limitations and verification results.
- `evaluation/metrics.json`: the actual 600-output mechanical audit.

The archive `output/zips/Small_Weather_Source.zip` contains source, data, documentation, tests, selected poems and the presentation assets needed for rebuilding. It excludes the virtual environment and temporary renders. `output/zips/Small_Weather_Presentation.zip` contains the anthology, all complete poem texts, the original illustrations, exact prompts and provenance. The source ZIP intentionally contains the images as well, making its optional anthology builder self-contained.

## Tests and evaluation

```sh
python3 -m unittest discover -s tests -v
python3 scripts/evaluate.py
python3 scripts/selection_bias.py
```

## Rebuild the report

Requires a LaTeX distribution with `pdflatex` (e.g. TeX Live or MiKTeX):

```sh
cd report
pdflatex report.tex && pdflatex report.tex
```

The tests check determinism, varied seeds, finite failure, invalid arguments, structural rules across all themes, and execution from another directory without overwriting an existing file. The audit compares 1 versus 48 candidates across seeds 0-99 in each theme. All 600 poems passed the mechanical rules; each 100-poem condition contained 100 distinct bodies. Line variety decreased with selection. No human reader study has been performed.

## Rebuild the poetry presentation (optional)

The finished PDF can be read without installing anything. Rebuilding it requires ReportLab; the generator itself does not.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-presentation.txt
.venv/bin/python scripts/build_anthology.py
python3 scripts/package.py
```

On Windows, substitute `.venv\Scripts\python.exe` for `.venv/bin/python`. The PDF and ZIP build scripts replace their own generated output files. They do not alter source poems or illustrations.

Optional PDF verification and preview rendering (Python 3.12 was used here):

```sh
.venv/bin/python -m pip install -r requirements-qa.txt
.venv/bin/python scripts/verify_artifacts.py --render-dir tmp/pdfs
```

Rebuilding uses the included PNGs and makes no generative AI calls. To create a different set of illustrations, use the saved prompts in an image-generation tool and record the new tool, prompts and assets; the poem seed is not an image seed. The current illustrations were produced through the built-in image generation tool, whose exact model identifier and image seed were not exposed.

## AI assistance and contribution

Codex assisted with the concept, source research, implementation, original grammar phrases, output review and project documentation. The Python program generated the final poem texts by recombination. The built-in image generation tool made one illustration for each selected poem, using the complete poem in its prompt. ReportLab placed the text and illustrations on the page without rewriting the poems. These are distinct stages; the runtime generator should not be described as an AI-free development effort or as a trained language model.

The source references and reflections are in `LOGBOOK.md`. Review and adapt this project, and describe personal contributions accurately when writing the report later.
