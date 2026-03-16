---
title: Contact
permalink: /contact/
intro: Professional contact details and researcher profiles.
---
{% assign profile = site.data.profile %}
{% assign links = site.data.links %}
{% assign sources = site.data.publication_sources %}

<div class="contact-grid">
  <article class="info-card">
    <h3>Email</h3>
    <p><a href="mailto:{{ profile.email }}">{{ profile.email }}</a></p>
  </article>
  <article class="info-card">
    <h3>Google Scholar</h3>
    <p><a href="{{ links.scholar }}">Scholar profile</a></p>
  </article>
  <article class="info-card">
    <h3>ORCID</h3>
    <p><a href="{{ links.orcid }}">{{ links.orcid }}</a></p>
  </article>
  <article class="info-card">
    <h3>GitHub</h3>
    <p><a href="{{ links.github }}">{{ links.github }}</a></p>
  </article>
  <article class="info-card">
    <h3>Scopus Author ID</h3>
    <p>{{ sources.scopus_author_id }}</p>
  </article>
  <article class="info-card">
    <h3>ResearcherID</h3>
    <p>{{ sources.researcher_id }}</p>
  </article>
</div>

## Affiliations

{% for affiliation in profile.affiliations %}
- {{ affiliation }}
{% endfor %}
