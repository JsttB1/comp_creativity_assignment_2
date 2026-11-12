# What is left

Status: 12 November 2026. See [what we have done](WHAT_WE_HAVE_DONE.md) for the completed implementation and presentation.

The main unfinished assignment deliverable is the **PDF report, maximum four pages, using the supplied course template**. You asked to leave it unwritten, so this file only records the remaining work.

## Required before submission

### 1. Obtain the report template

- [ ] Find the template referenced in the assignment brief. It has not been supplied in this workspace.
- [ ] Check the template's required headings and identification fields.

### 2. Write the report when you are ready

- [ ] Use the required template and keep the final PDF within four pages.
- [ ] Explain the creative system and give a brief, step-by-step account of the work.
- [ ] Explain the inspiring-set choices and how they shaped the generator.
- [ ] Describe the grammar, generation stopping criteria, candidate selection and important implementation decisions.
- [ ] Reflect on challenges, limitations and your own contribution to the process.
- [ ] Explain how generative AI produced the presentation of all three poems and reflect on the results.
- [ ] Clearly distinguish the Python poem generator from image generation, and accurately describe Codex's development assistance.
- [ ] Conclude with a reflection on evaluating the system's creativity. Use the existing mechanical audit as limited evidence; do not equate its scores or unique outputs with creative quality.

Material already available for this work:

| Topic | Existing evidence |
| --- | --- |
| Inspiration, initial design, changes and reflections | [LOGBOOK.md](LOGBOOK.md) |
| Algorithm and stopping criteria | [poet.py](poet.py), [data/grammar.json](data/grammar.json), [README.md](README.md) |
| Generated poems and reproducibility | [poems/selected.json](poems/selected.json) |
| Generative AI presentation process | [presentation/README.md](presentation/README.md), [prompts](presentation/prompts), [provenance](presentation/provenance.json) |
| Evaluation results and limitations | [evaluation/metrics.json](evaluation/metrics.json), logbook sections 5-6 |

### 3. Review the final submission materials

- [ ] Review the code, poems, images and documentation and make any desired personal revisions.
- [ ] Check that the report describes the actual final implementation and your own experience accurately.
- [ ] If changing poems, grammar or illustrations, update dependent presentation files, prompts, metadata and hashes before rebuilding and verifying the packages. Rerunning the layout alone does not update provenance.
- [ ] If only changing documentation, rebuild the ZIPs with `python3 scripts/package.py` so the source archive contains the latest files.
- [ ] Inspect the finished report PDF for its page count, layout and template compliance.

The current generator and presentation already meet the corresponding requirements in the provided brief. Revisions here are a final review step, not evidence of a known missing generator feature.

### 4. Submit the three requested deliverables

- [ ] Final report PDF: still to be created.
- [ ] [Source ZIP](output/zips/Small_Weather_Source.zip): already prepared.
- [ ] [Presentation ZIP](output/zips/Small_Weather_Presentation.zip): already prepared, including complete texts of all three poems.

Confirm the submission destination and deadline through the course materials; neither is specified in the provided Markdown brief. Pushing the project to a Git remote does not submit the assignment to the course.

## Optional improvements, not missing requirements

- Run a small blind reader study comparing coherence, surprise, imagery and emotional effect.
- Compare illustrated and plain-text versions to investigate how presentation changes perceived value.
- Reduce repeated phrases across different poems; the current check only rejects duplicate lines within an individual poem.
- Expand the phrase banks, themes or inspiring set and examine whether diversity improves without reducing coherence.

The assignment permits a reflection on creativity evaluation without conducting a reader study. These extensions are optional; the report and final submission are the remaining required work.
