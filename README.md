# Alexei Kornaev Academic Website

This repository contains a minimal Jekyll-based academic website prepared for GitHub Pages deployment.

## Stack

- Jekyll
- `minima` as the base theme
- `jekyll-scholar` for BibTeX-driven publications
- GitHub Actions for build and deploy

## Repository structure

- `_data/profile.yml` - main personal metadata
- `_data/links.yml` - external links and contact targets
- `_data/publication_sources.yml` - publication source identifiers
- `_data/publication_overrides.json` - optional per-publication links and manual metadata
- `_data/publications.json` - generated structured publication data
- `_data/theses.yml` - thesis list for manual editing
- `bibliography/publications.bib` - single source of truth for publications
- `teaching/cv-2026/` - imported Computer Vision 2026 course project with LaTeX sources and weekly materials
- `scripts/sync_publications.py` - syncs publications from ORCID into BibTeX and site data
- `assets/css/style.scss` - site styles
- `assets/img/` - images and placeholders
- `_layouts/` - lightweight custom layouts
- `index.md` and top-level `*.md` pages - editable page content

## Local development

1. Install Ruby and Bundler.
2. Install dependencies:

```bash
bundle install
```

3. Start the local server:

```bash
bundle exec jekyll serve
```

4. Open `http://127.0.0.1:4000`.

## Publication sync

The repository includes an automated ORCID-based sync script.

Run it locally with:

```bash
py -3 scripts/sync_publications.py
```

This updates:

- `bibliography/publications.bib`
- `_data/publications.json`

Notes:

- ORCID is the supported automatic source because it has a public API.
- Google Scholar does not provide an official public API, so scraping it reliably over time is not recommended.
- Scopus and Web of Science are linked via your identifiers, but full automated harvesting from those services usually requires API access and credentials.
- Add paper/code/project/slides/dataset links in `_data/publication_overrides.json` when ORCID/Crossref metadata does not contain them.

## Deployment

The site includes a GitHub Actions workflow in `.github/workflows/deploy.yml`.

To deploy on GitHub Pages:

1. Push this repository to GitHub.
2. In GitHub, open `Settings -> Pages`.
3. Set the source to `GitHub Actions`.
4. Push to the default branch.

The workflow will build the Jekyll site with `jekyll-scholar` and publish it.
The repository also includes a scheduled workflow that refreshes publications from ORCID once per week and can be triggered manually.

## What to edit first

1. Replace profile details in `_data/profile.yml`.
2. Update external links in `_data/links.yml`.
3. Add real publications in `bibliography/publications.bib`.
4. Replace the placeholder CV file at `assets/files/alexei-kornaev-cv.pdf`.
5. Replace the placeholder profile image at `assets/img/profile-placeholder.svg` if desired.
6. Edit page content in:
   - `index.md`
   - `research.md`
   - `teaching.md`
   - `software.md`
   - `contact.md`
7. Add private application documents in ignored folders such as `job-search/` if you want to keep teaching/research statements in the same repository without publishing them.

## Adding Russian pages later

The current structure keeps content in standalone Markdown pages and centralizes profile data in `_data/`.
To add Russian pages later, create parallel pages such as `index.ru.md`, `research.ru.md`, and a matching Russian navigation pattern without changing the publication or data model.
