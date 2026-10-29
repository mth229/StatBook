# CLAUDE.md — guidance for Claude Code in this repository

## What this is
An introductory statistics textbook written as a Quarto **book** project,
written collaboratively by several authors and published to GitHub Pages by
`.github/workflows/publish.yml`. Audience: first-year undergraduates with no
calculus assumed.

## Layout
- `_quarto.yml` — book config and chapter order. **New chapters must be added here.**
- `index.qmd` — preface. `chapters/NN-slug.qmd` — one file per chapter.
- `apps-src/*.py` — marimo notebooks, exported to WebAssembly at
  `_book/apps/<name>/` by `scripts/build_apps.py` (Quarto post-render hook).
  Embed in a chapter with an `<iframe src="../apps/<name>/index.html">`.
- `_extensions/r-wasm/live/` — the quarto-live extension (vendored; don't edit).
  The book format is `live-html`, enabling in-browser `{webr}` / `{pyodide}`
  cells. Example: `chapters/03-practice-describing-data.qmd`.
- `references.bib` — shared BibTeX; cite as `[@key]`.
- Dependencies: R → `DESCRIPTION` (Imports), Julia → `Project.toml`
  (+ `Manifest.toml`), Python/apps → `pyproject.toml` (uv).
- `_book/`, `_freeze/`, `.quarto/` are generated — never edit or commit them.

## Commands
- Preview while writing: `quarto preview`
- Render one chapter: `quarto render chapters/02-describing-data.qmd`
- Full build (what CI runs): `quarto render`
- Edit an app: `uv run marimo edit apps-src/clt_demo.py`
- Rebuild apps only: `BUILD_APPS=1 python scripts/build_apps.py`
- Add R pkg: add to `DESCRIPTION` Imports. Add Julia pkg:
  `julia --project=. -e 'using Pkg; Pkg.add("Name")'`.

## Conventions
- **One computational language per chapter.** R chapters set `engine: knitr`;
  Julia chapters set `engine: julia` with `julia: exeflags: ["--project=@."]`.
  State the language in a callout at the top of the chapter.
- Every chapter has a `{#sec-slug}` id on its title. Cross-reference with
  `@sec-…`, `@fig-…`, `@tbl-…`, `@eq-…`. Figure chunks use `#| label: fig-…`
  and `#| fig-cap:`.
- Use `#|` chunk options, not knitr inline chunk headers.
- Set a seed (`set.seed()` / `Random.seed!()`) before any simulation.
- Notation (see `chapters/01-introduction.qmd`, @tbl-notation): $\mu,\sigma,p$
  for parameters; $\bar{x}, s, \hat{p}$ for statistics. Don't introduce
  alternatives.
- Prose: plain, friendly, second person ("you"). Define every term in bold at
  first use. End each chapter with an `## Exercises` section.
- Live (in-browser) cells: the chapter uses `engine: knitr`, lists browser
  packages under `webr: packages:` / `pyodide: packages:`, and includes
  `{{< include ../_extensions/r-wasm/live/_knitr.qmd >}}` right after the
  YAML. Exercise ids are unique across the book and look like `ex_<topic>`;
  every exercise gets a `.hint` or `.solution` div, and a `#| check: true`
  cell (using `.result`) when the answer is checkable. Live and ordinary
  `{r}` cells may share a chapter, but `{r}` output is computed at build time.
- marimo apps: only use packages available in Pyodide; keep them small; fixed
  seeds; every app must be referenced from at least one chapter.

## When editing
- Keep changes scoped to what was asked; don't reflow paragraphs you didn't
  change (it makes co-authors' diffs hard to review).
- After editing a chapter, render that chapter to confirm it builds.
- Don't change `_quarto.yml` theme/format settings or the CI workflow unless asked.
