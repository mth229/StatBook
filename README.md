# Introductory Statistics — an open, collaborative textbook

Written in [Quarto](https://quarto.org), with examples in **R** and **Julia**
and in-browser interactive apps built with [marimo](https://marimo.io)
(Python → WebAssembly). Every push to `main` is rendered by GitHub Actions and
published to GitHub Pages.

## Repository layout

```
_quarto.yml              Book configuration + chapter order
index.qmd                Preface
chapters/NN-slug.qmd     One file per chapter (R *or* Julia per chapter)
references.qmd/.bib      Bibliography
_extensions/r-wasm/live/ quarto-live extension (in-browser R/Python exercises)
apps-src/*.py            marimo notebooks → exported to _book/apps/<name>/
scripts/build_apps.py    Quarto post-render hook that exports the apps
DESCRIPTION              R packages the book needs
Project.toml             Julia packages the book needs (commit Manifest.toml too)
pyproject.toml           Python deps for the apps (managed with uv)
CLAUDE.md                Project instructions read by Claude Code
.claude/settings.json    Shared Claude Code permissions
.github/workflows/       CI: render on every PR, publish from main
```

## One-time setup (each author)

1. **Quarto** ≥ 1.5 — <https://quarto.org/docs/get-started/>
2. **R** (only if you write R chapters):
   `Rscript -e 'install.packages("pak"); pak::local_install_deps()'`
3. **Julia** ≥ 1.10 (only if you write Julia chapters; Quarto's Julia engine
   is built in — no IJulia/Jupyter needed):
   `julia --project=. -e 'using Pkg; Pkg.instantiate()'`
4. **uv** (only if you work on apps): <https://docs.astral.sh/uv/> then `uv sync`

Check everything with `quarto check`.

## Everyday workflow

```bash
git switch -c ch05-confidence-intervals
quarto preview                      # live-reloading preview in the browser
# … write …
quarto render chapters/05-*.qmd     # confirm the chapter builds
git push -u origin HEAD             # open a pull request; CI renders the whole book
```

Merge to `main` → the site updates in a couple of minutes.

### Adding a chapter
1. Create `chapters/NN-slug.qmd` with a title like `# Topic {#sec-slug}`.
2. For code, put `engine: knitr` (R) or `engine: julia` (Julia) in its YAML
   header — see chapters 02 and 04. Don't mix languages in one chapter.
3. Add it to `book.chapters` in `_quarto.yml`.
4. New packages → `DESCRIPTION` (R) or `Pkg.add` (Julia).

### Adding an interactive app
1. `uv run marimo edit apps-src/my_app.py` — build the app in the marimo editor.
2. Embed it in a chapter:
   ```html
   <iframe src="../apps/my_app/index.html" style="width:100%;height:700px"></iframe>
   ```
3. `quarto render` exports it automatically. Only use packages available in
   [Pyodide](https://pyodide.org/en/stable/usage/packages-in-pyodide.html).

### Adding in-page exercises (quarto-live)
The [quarto-live](https://r-wasm.github.io/quarto-live/) extension (in
`_extensions/r-wasm/live/`, committed to the repo) puts editable, runnable R
(webR) or Python (Pyodide) cells directly in a chapter, plus auto-graded
exercises with hints and solutions. See `chapters/16-practice-describing-data.qmd`.

1. In the chapter's YAML header set `engine: knitr` and list browser packages
   under `webr: packages:` (or `pyodide: packages:`).
2. Right after the header add
   `{{< include ../_extensions/r-wasm/live/_knitr.qmd >}}`.
3. Use ```` ```{webr} ```` cells. For an exercise add `#| exercise: <id>`,
   with `::: {.hint exercise="<id>"}` / `::: {.solution exercise="<id>"}` divs
   and an optional `#| check: true` grading cell.

The book's format is `live-html` (in `_quarto.yml`), which is ordinary HTML
plus this extension. To update the extension: `quarto update r-wasm/quarto-live`.
There is no in-browser Julia runtime, so live cells are R or Python only.

## Rendering and caching

`execute: freeze: auto` re-runs a chapter's code only when the chapter
changes, which keeps local previews fast. `_freeze/` is **not** committed: CI
installs R, Julia and Python and re-executes everything from scratch, so the
published book always reflects the committed code. If CI gets slow later,
switch strategy: commit `_freeze/` and drop the R/Julia setup steps from the
workflow (authors then render locally before pushing).

## Using Claude from IntelliJ IDEA

1. Install Claude Code (<https://docs.claude.com/en/docs/claude-code>) and the
   **Claude Code** plugin from the JetBrains Marketplace.
2. Open this folder in IntelliJ, open the built-in terminal at the project
   root and run `claude`. The plugin connects it to the editor (open files,
   selections, diffs shown in IntelliJ's diff viewer).
3. Claude reads `CLAUDE.md` automatically, so it knows the conventions,
   chapter structure and build commands. Keep that file up to date — it is
   the shared "style guide" for every author *and* for Claude.
4. `.claude/settings.json` (committed) pre-approves safe commands such as
   `quarto render`; personal overrides go in `.claude/settings.local.json`
   (git-ignored).

Helpful IntelliJ setup: associate `*.qmd` with the Markdown file type
(Settings → Editor → File Types → Markdown), and install the R Language and
Julia plugins if you want highlighting/run support for scripts.

## GitHub setup (once, by the repo owner)

1. Create an empty repo, then from this folder:
   ```bash
   git init -b main && git add . && git commit -m "Initial book scaffold"
   git remote add origin git@github.com:OWNER/REPO.git
   git push -u origin main
   ```
2. **Settings → Pages → Build and deployment → Source: GitHub Actions.**
3. Replace `OWNER/REPO` in `_quarto.yml` (`repo-url`, `site-url`).
4. Recommended: **Settings → Branches** → protect `main`, require a pull
   request and the *Render book / render* check to pass.
5. Add colleagues under **Settings → Collaborators**.

## License

Choose a license before publishing (for open textbooks, CC BY 4.0 for text
and MIT for code is common) and add it as `LICENSE`.
