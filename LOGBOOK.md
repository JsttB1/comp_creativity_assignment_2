# Small Weather - development logbook

This is a factual project log, not the assignment report or a claim about the student's personal experiences. Work below was carried out with Codex assistance on 12 November 2026. The user requested that the report be left unwritten.

## 1. Initial idea and inspiring set

Create eight-line English poems in which ordinary objects hold an emotional trace. Use three settings: a rainy street (waiting), a misty harbour (release), and a frosted garden (return). Aim for restrained free verse, concrete sensory details, an emotional turn, and a recurring object. Rhyme and a fixed metre are not requirements.

The following three poems were read online on 12 November 2026. These are design references, not a training set or a database loaded by the program. No complete source poem or copied source line is included in the generator's data.

| Poem and source | Observation / interpretation | Design decision |
| --- | --- | --- |
| Carl Sandburg, [Fog](https://poets.org/poem/fog), Academy of American Poets | A compact weather image becomes an animate presence; the city gives it a concrete setting. | Keep poems brief and let weather perform an action. Do not reuse the cat metaphor. |
| Emily Dickinson, [Beclouded](https://etc.usf.edu/lit2go/114/the-poems-of-emily-dickinson-series-one/2632/nature-poem-29-beclouded/), first line “The sky is low, the clouds are mean”, Lit2Go, University of South Florida | Weather behaves like a person with a mood. The small scene can carry a wider emotional implication. | Give objects human verbs, then introduce a reflective speaker. Do not imitate Dickinson's rhyme or punctuation. |
| Sara Teasdale, [There Will Come Soft Rains](https://poets.org/poem/there-will-come-soft-rains), Academy of American Poets | Sensory natural details lead to a change of perspective about human presence. | Move from observation to a turn and end with an image that continues beyond the speaker. Do not reproduce the poem's war setting or rhyming couplets. |

These interpretations motivate a deliberately narrow aesthetic; they do not establish that the generator matches the quality of the sources. The set is small and limited to English-language examples. A wider set could support different voices, cultures and forms. Source texts remain available at the links above; the runtime is fully offline.

## 2. Initial generator design

**Approach:** a finite, parameterised grammar with small theme-specific phrase banks, followed by bounded generate-and-select. Python was chosen for a readable implementation that requires no external packages to generate poems. A Markov chain over only three short sources would have little evidence for fluent transitions and could overuse the original wording. A runtime language model would make the relationship between the inspiring set and the generated text harder to trace. These are design judgements, not comparative experimental results.

**Planned structure:** four couplets, eight lines in total.

1. Establish weather and place.
2. Introduce a concrete object with a human memory or action.
3. Add a sound.
4. Add a visual detail.
5. Introduce an emotional turn in the speaker's perspective.
6. Let the environment respond through a counterpoint.
7. Return to the same object.
8. Close on a continuing physical image.

The object is selected once per candidate and reused. Vocabulary for weather, place, details and closure comes from one theme. All motif noun phrases are singular, and their adjectives are chosen as pairs to keep agreement and imagery manageable. The opening alternatives use third-person singular verbs; generic actions use compatible memory noun phrases.

**Stopping rules:** finish each candidate after eight lines; attempt exactly the requested number of candidates (default 48, maximum 1,000); return the highest-scoring valid candidate, breaking ties in favour of the earliest candidate. If none passes the mechanical rules, return a clear error. A CLI invocation produces exactly `--count` poems (1-100). There is no recursive or unbounded generation loop.

## 3. Implementation decisions

- The theme banks and templates live in `data/grammar.json` so they can be inspected and changed without editing algorithm code.
- Runtime generation uses `random.Random(seed)` locally. JSON exports record the seed, theme, grammar digest, version, candidate budget and winning candidate index. The same code, grammar and compatible Python random implementation reproduce the result.
- Validation rejects duplicate lines, unresolved placeholders, missing motif recurrence and lines outside 4-14 words. It does not understand meaning.
- The selector prefers lengths near seven words, penalises repeated content words outside the motif, and slightly rewards adjacent alliteration. Its numeric score measures those preferences only; it is not a validated creativity score.
- Presentation images will be made from the actual saved poems. Poem text will be placed separately as selectable text in the anthology so that image generation cannot misspell or silently rewrite the poems.
- The source-poem links and inspirations are kept in this logbook rather than bundled as a scraped corpus.

## 4. Authorship and AI assistance

Codex assisted with choosing this initial concept, researching the references, writing the code, composing the original phrase banks, checking outputs and writing this logbook. Therefore, this is **not** an AI-free development process. At runtime, the Python generator recombines its saved grammar without a model or network call. A separate generative image tool is used for the presentation; its exact prompts and outputs are recorded with the presentation. The student should review, understand and adapt the work and describe their own contribution accurately in any later report.

## 5. Evaluation plan and limitations

First check reproducibility, finite stopping, grammatical constraints and diversity across a fixed set of seeds. These establish technical behaviour, not artistic value. Inspect both successes and awkward lines, including weak combinations that still pass the rules.

For a future reader study, sample poems with a predeclared seed schedule. Compare `--candidates 1` with the default 48-candidate selector using blind ratings of coherence, surprise, imagery and emotional effect. Do not tell raters which condition produced a poem. Separately compare plain text with illustrated versions, counterbalancing order, to examine whether presentation changes perceived value. Report sample size, disagreements and limitations. No reader study has been performed at this stage.

The main creative limitation is that the design fixes the structure, themes and many phrases. Search can rearrange the available material but cannot invent a new form or evaluate a reader's interpretation. An illustration may add polish and impose a literal reading on an ambiguous poem. Neither uniqueness in a sample nor a high heuristic score proves originality or creativity.

## 6. Actual outputs and mechanical audit - 12 November 2026

The first anthology uses rain/42, tide/43 and frost/44, with the default 48 candidates. The candidate winners were respectively 28, 18 and 23. Titles are **Rain / ticket**, **A place for sea mist**, and **Frost / gate**. The poems are saved unchanged, with metadata, in `poems/selected.json`. No hand editing or post-generation seed search was used to improve this trio.

The six unit tests passed, including checks across 150 theme/seed combinations. A separate audit generated 100 poems per theme with each of two candidate budgets: 600 outputs in total. Every output passed the mechanical checks, and every condition contained 100 different poem bodies. Results are reproducible through `scripts/evaluate.py` and are stored in `evaluation/metrics.json`.

| Theme | Mean heuristic score, 1 / 48 candidates | Distinct lines out of 800, 1 / 48 candidates |
| --- | --- | --- |
| Rain | 87.62 / 94.81 | 180 / 154 |
| Tide | 81.33 / 90.06 | 180 / 167 |
| Frost | 80.28 / 89.51 | 180 / 163 |

The score improvement is expected: the selector optimises that exact score, so it is not independent evidence of quality. It also reduces line diversity in all three themes. A future revision could cap cross-poem phrase reuse or compare a different critic in a blind reader study. The current version keeps the limitation visible instead of claiming novelty from combinatorial counts.

Output review also found two limitations that the mechanical checks miss. The city and garden poems use the same reflective line about leaving; validation prevents duplicate lines within a poem, not between poems. In the harbour poem, the boat turns towards open water while also waiting. That tension may be read as evocative or inconsistent; the program cannot judge which. The garden poem's hidden letters and deciding root give the scene a linked metaphor, but this is an interpretation by the reviewer, not evidence of system understanding.

## 7. Generative AI presentation - 12 November 2026

One original illustration was generated per poem with the built-in `image_gen.imagegen` tool. Exact prompts are saved in `presentation/prompts/` and include the complete texts. A shared gouache/ink treatment and muted palette connect the images. Each prompt also names a concrete object and setting: ticket under a bridge, boat below a pier, gate beside a greenhouse. The first image from each prompt was retained, without edits. The provider did not expose an exact model identifier or an image seed; this is recorded rather than guessed.

Visual review found each central object and setting present. The rain image makes the departure image more tangible through the small ticket and reflected window. The harbour image depicts stillness and tethering but cannot directly convey forgiveness. The garden image visualises hidden growth with exposed roots, making the poem more literal. This illustrates a presentation tradeoff: visual consistency may make the collection inviting while narrowing the range of imagined scenes. No claim is made that readers actually valued the illustrated poems more; that would require evaluation.

Poem text is typeset separately using ReportLab so every line remains selectable and exact. The image assets are preserved unchanged. File hashes in `presentation/provenance.json` link every poem, prompt and illustration. Generating an image from the same prompt is not guaranteed to reproduce the same pixels.

The local PDF dependencies were initially unavailable; installation into a project-local virtual environment resolved that. Poppler was unavailable, so PyMuPDF is used for page rendering and pypdf for text checks. This affects presentation tooling only; poem generation still needs only the Python standard library.

## 8. Verification and delivery state

All six unit tests passed under both Python 3.15.2 and Python 3.12.10. The three selected JSON records reproduced exactly in both environments. PDF checks confirmed all titles and poem lines were present, all asset hashes matched, and text stayed within page bounds. All three rendered pages were visually inspected. An initial letter-spacing state leak affected headers and subsequent text; isolating the tracked header text fixed it, and the revised pages were rendered and inspected again.

Both ZIPs passed integrity checks. The extracted source ran with Python site-packages disabled and reproduced all three selected poems, confirming that the generator requires only the standard library. Using the optional presentation dependencies, the extracted source rebuilt a byte-identical anthology PDF. The presentation archive was checked for three illustrations and the complete text of every poem.

Delivered files are `output/zips/Small_Weather_Source.zip`, `output/zips/Small_Weather_Presentation.zip`, and the preview `output/pdf/Small_Weather_Anthology.pdf`. No report was created, in accordance with the user's instruction. The report/template requirement remains a separate, deferred assignment item.
