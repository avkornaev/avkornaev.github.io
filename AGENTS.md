# AGENTS.md

## Project purpose
This repository hosts the personal academic website of Alexei Kornaev.
The site should present biography, publications, research directions, teaching, software, and contact information.
The site must be suitable for GitHub Pages deployment and easy to maintain by one researcher.

## Current architecture to preserve
This repository already uses:
- Jekyll
- GitHub Pages deployment via GitHub Actions
- BibTeX as the publication source of truth
- jekyll-scholar for rendering bibliography
- data files in `_data/`
- content pages in top-level `.md` files

Do not replace this stack unless explicitly requested.
Do not migrate the site to another generator or framework.
Do not introduce a CMS or JS-heavy frontend.

## Priorities
1. Clarity over cleverness.
2. Stability over novelty.
3. Simple editable content over hidden logic.
4. Publications must come from a single source of truth.
5. The site should be easy to extend with new papers, courses, and projects.
6. Public-facing pages must not contain placeholder text or local filesystem links.

## Stack rules
- Prefer GitHub Pages-compatible Jekyll setup.
- Prefer simple layouts and minimal dependencies.
- Avoid custom build steps unless clearly necessary.
- Avoid heavy JavaScript frameworks.
- Use BibTeX as the source of truth for publications where practical.
- Keep content in clearly named markdown, yaml, and bib files.
- Preserve GitHub Actions deployment.
- Preserve jekyll-scholar unless explicitly asked to replace it.

## Content structure
The site should contain:
- Home
- Publications
- Research
- Teaching
- Software
- CV
- Contact

## Editing principles
- Do not rewrite the entire site when only one section needs changes.
- Preserve user content unless explicitly asked to replace it.
- Keep filenames and directory names semantically clear.
- Add comments in config files only when they help future editing.
- Remove placeholder text from public pages when replacing sections.
- Never add local filesystem paths such as `G:/...` or `C:/...` to public links.

## Publication handling
- Use a dedicated bibliography file.
- Each publication entry should support links to paper, code, project page, slides, and dataset when available.
- Keep publication metadata normalized and easy to update.
- Prefer visitor-facing clarity over explaining internal sync mechanics.

## Style guidance
- Academic, minimal, professional.
- No marketing language.
- Short paragraphs, high information density.
- Emphasize research problems, contributions, and artifacts.
- Prefer concrete research directions over generic future-looking placeholders.

## Output expectations for agent tasks
When asked to make changes:
1. state which files will be changed
2. make the smallest sound set of edits
3. preserve buildability
4. summarize what the user should edit next

## Non-goals
- No blog engine unless explicitly requested
- No CMS
- No animation-heavy landing page
- No unnecessary dependency on external services