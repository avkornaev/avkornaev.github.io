# Alexei Kornaev

Research Scientist in Physics and AI, including Deep Learning, Computer Vision, Physics-informed Neural Networks, AI in Medicine, and Robotics.

Personal website: [avkornaev.github.io](https://avkornaev.github.io)

## About

Alexei Kornaev works at the intersection of artificial intelligence, computer vision, medical AI, physics-informed machine learning, and robotics. His research focuses on methods that are both mathematically grounded and useful in real-world scientific and clinical settings.

Current affiliations:

- Center for Top-Level Educational Programs in AI, Innopolis University, Innopolis, Republic of Tatarstan, Russia
- N.N. Blokhin National Medical Research Center of Oncology, Moscow, Russia

## Research interests

- Computer vision for clinical decision support
- Foundation models for medical imaging
- Physics-informed neural networks and AI-empowered physics
- Multimodal learning for healthcare
- Reliable AI for real-world deployment
- Robotics

## Links

- Website: [avkornaev.github.io](https://avkornaev.github.io)
- Google Scholar: [Scholar profile](https://scholar.google.com/citations?user=TGYOzQEAAAAJ&hl=ru)
- ORCID: [0000-0001-5121-6045](https://orcid.org/0000-0001-5121-6045)
- GitHub: [avkornaev](https://github.com/avkornaev)
- Email: [a.kornaev@innopolis.ru](mailto:a.kornaev@innopolis.ru)

## Website sections

- Home: short biography, research agenda, affiliations, and overview
- Publications: publications synchronized from ORCID and exported to BibTeX
- Research: current directions and project summaries
- Teaching: courses, materials, and supervision
- Software: repositories, datasets, and demos
- CV: downloadable CV
- Contact: professional links and contact information

## Repository note

This repository contains the source code and content for the website. Publications are maintained through an ORCID-based synchronization workflow and stored in BibTeX for use by the Jekyll site.

## Local build

Install dependencies and run the local server:

```bash
bundle install
bundle exec jekyll serve
```

The site will be available at `http://127.0.0.1:4000`.

## Deployment

Deployment is handled through GitHub Actions for GitHub Pages.

To publish:

1. Push the repository to GitHub.
2. In the repository settings, open `Pages`.
3. Set the source to `GitHub Actions`.
4. Push changes to the default branch.

For the user site at `https://avkornaev.github.io`, the repository should remain named `avkornaev.github.io`.

## Publication maintenance

Edit `bibliography/publications.bib` to maintain publication facts and links.
This curated bibliography is the source of truth. Rebuild the website data and
copy-paste-ready Markdown export without network access:

```bash
python3 scripts/sync_publications.py --offline
```

This generates:

- `_data/publications.json`
- `generated/publications.md` (excluded from Jekyll publishing)

Do not restore a second `_data/publications.yml`: Jekyll loads both files under
the same data key, which can mask newer records. The old enrichment snapshot and
the 25 October 2026 import decisions remain in `_publication_imports/`, which
Jekyll does not publish. Rows marked `TODO-check` there require review before
adding them to the public bibliography.

To merge new ORCID works and fill empty fields in existing records:

```bash
python3 scripts/sync_publications.py
```

Existing local fields take priority, so scheduled ORCID updates preserve manual
corrections and publications absent from ORCID. Works are matched by normalized
DOI or title; identical-title preprints can be linked with a `preprint` field.
ORCID entries without author metadata are skipped with a warning; supply a
verified author list in the overrides or curated BibTeX before importing them.
The script uses only the Python standard library. Use literal BibTeX fields,
not `@string` macros or string concatenation. Optional fields include `paper`,
`code`, `project`, `slides`, `dataset`, `preprint`, and `category`.

Run maintenance checks with `python3 -m unittest discover -s scripts -p 'test_*.py'`.
The scheduled GitHub Actions workflow runs the ORCID merge and commits its outputs.
