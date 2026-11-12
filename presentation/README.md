# Small Weather - poetry presentation

Open **Small_Weather_Anthology.pdf** in this ZIP to read the three illustrated poems. In the working project, the PDF is under `output/pdf/`.

| Page | Poem | Theme | Generator seed |
| --- | --- | --- | --- |
| 1 | Rain / ticket | Rainy city; waiting | 42 |
| 2 | A place for sea mist | Harbour; release | 43 |
| 3 | Frost / gate | Frosted garden; return | 44 |

The complete texts are in `texts/` and `selected.json` (in the ZIP). The original AI illustrations are in `images/`, and their exact prompts are in `prompts/`. No image text is needed to recover the poems: the anthology contains selectable text and the archive includes plain-text copies.

## How the presentation was made

1. `poet.py` generated these three poems with the original saved grammar, using 48 candidates per poem. The seeds were consecutive, beginning at 42; the finished texts were not edited or selected from a larger gallery.
2. Each complete poem was included verbatim in a separate prompt to the built-in `image_gen.imagegen` tool on 12 November 2026. Shared instructions requested quiet gouache and ink illustrations in muted slate, teal, ivory and ochre. Scene descriptions emphasised each poem's object and setting.
3. Each prompt produced one image. The first output for each was retained. The files were copied unchanged into this project. The exact underlying model identifier and image seed were not exposed by the tool.
4. A Python/ReportLab layout placed the original illustrations above the complete poem texts. Titles, line breaks and stanza gaps come from the generator. The image tool did not typeset or rewrite the poems.

`provenance.json` connects each illustration to its prompt, poem and generator metadata, including SHA-256 hashes. The seed reproduces the poem with the same generator; it does not reproduce the illustration.

Codex assisted with the generator's design, original phrase banks, implementation, image prompts and layout. The generator runs without an LLM or API, while the presentation uses generative AI imagery. This is the poetry presentation only; it is not the assignment report.
