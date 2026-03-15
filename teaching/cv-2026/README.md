# CV-2026

Portable LaTeX lecture sources now live in `sources/`.

The repository keeps two parallel views of the course:

- `Week_01` ... `Week_15` are student-facing delivery folders for PDFs and notebooks.
- `sources/` is the self-contained LaTeX authoring project that can be opened in Cursor, copied into Overleaf/Prism, or versioned here.

## LaTeX Authoring Layout

- `sources/template.tex`: shared document skeleton used by every lecture
- `sources/style.sty`: shared style, packages, macros, and defaults
- `sources/references.bib`: shared bibliography for all lectures
- `sources/figures/`: shared figure folder for all lectures
- `sources/syllabus/`: syllabus source files
- `sources/week_01` ... `sources/week_15`: one lecture root per week

## Workflow

Open `sources/` in Cursor and compile any `sources/week_XX/main.tex` with LaTeX Workshop.
Each week folder has:

- `main.tex`: the compile target and lecture metadata
- `content.tex`: week-specific content

All paths are relative to `sources/`, so that folder can be copied into Overleaf or Prism without restructuring.

If `latexmk` is unavailable locally, the project still compiles with:

1. `pdflatex main.tex`
2. `biber main`
3. `pdflatex main.tex`
4. `pdflatex main.tex`
