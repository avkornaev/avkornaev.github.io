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
- `bibliography/publications.bib` - single source of truth for publications
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

## Deployment

The site includes a GitHub Actions workflow in `.github/workflows/deploy.yml`.

To deploy on GitHub Pages:

1. Push this repository to GitHub.
2. In GitHub, open `Settings -> Pages`.
3. Set the source to `GitHub Actions`.
4. Push to the default branch.

The workflow will build the Jekyll site with `jekyll-scholar` and publish it.

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

## Adding Russian pages later

The current structure keeps content in standalone Markdown pages and centralizes profile data in `_data/`.
To add Russian pages later, create parallel pages such as `index.ru.md`, `research.ru.md`, and a matching Russian navigation pattern without changing the publication or data model.
