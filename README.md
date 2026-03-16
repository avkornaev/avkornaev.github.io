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

Publications are synchronized from ORCID into:

- `bibliography/publications.bib`
- `_data/publications.json`

Run the sync locally with:

```bash
py -3 scripts/sync_publications.py
```

The repository also includes a scheduled GitHub Actions workflow for regular ORCID updates.
