---
title: Publications
permalink: /publications/
intro: Publications are synced from ORCID into BibTeX and structured site data. Use the year filter for a recent subset, and keep optional links in the publication overrides file.
---
{% assign publication_items = site.data.publications.items | sort: "year" | reverse %}
{% assign thesis_items = site.data.theses | sort: "year" | reverse %}

<section class="section-block">
  <h2>Filter by year</h2>
  <div class="filter-bar">
    <label for="publication-year-filter">Show publications from year:</label>
    <select id="publication-year-filter">
      <option value="">All years</option>
      {% assign years = publication_items | map: "year" | uniq | sort | reverse %}
      {% for year in years %}
        <option value="{{ year }}">{{ year }} and later</option>
      {% endfor %}
      {% if years.size > 4 %}
        <option value="{{ years[4] }}">Last 5 years (approx.)</option>
      {% endif %}
    </select>
  </div>
</section>

<section class="section-block">
  <h2>Filtered publication list</h2>
  <div id="publication-results">
    {% for item in publication_items %}
      {% unless item.category == "conference" or item.category == "thesis" %}
        <article class="publication-item js-publication-item" data-year="{{ item.year }}">
          <div class="publication-citation">
            <strong>{{ item.title }}</strong><br>
            {% assign author_names = item.authors | map: "full" | join: ", " %}
            {{ author_names }}.
            {% if item.venue %}<em>{{ item.venue }}</em>. {% endif %}
            {{ item.year }}.
          </div>
          <div class="publication-links">
            {% if item.paper %}<a href="{{ item.paper }}">Paper</a>{% endif %}
            {% if item.code %}<a href="{{ item.code }}">Code</a>{% endif %}
            {% if item.project %}<a href="{{ item.project }}">Project</a>{% endif %}
            {% if item.slides %}<a href="{{ item.slides }}">Slides</a>{% endif %}
            {% if item.dataset %}<a href="{{ item.dataset }}">Dataset</a>{% endif %}
            {% if item.doi %}<a href="https://doi.org/{{ item.doi }}">DOI</a>{% endif %}
          </div>
        </article>
      {% endunless %}
    {% endfor %}
  </div>
  <p id="publication-empty" class="muted-text" hidden>No publications match the selected year range.</p>
</section>

<section class="section-block">
  <h2>Conference papers</h2>
  <ul class="list-clean">
    {% assign conferences = publication_items | where: "category", "conference" %}
    {% for item in conferences %}
      <li>
        <strong>{{ item.title }}</strong>, {% if item.venue %}<em>{{ item.venue }}</em>, {% endif %}{{ item.year }}.
        {% if item.doi %}<a href="https://doi.org/{{ item.doi }}">DOI</a>{% endif %}
      </li>
    {% endfor %}
    {% if conferences.size == 0 %}
      <li>Conference entries will appear here when available in ORCID or publication overrides.</li>
    {% endif %}
  </ul>
</section>

<section class="section-block">
  <h2>Theses</h2>
  <ul class="list-clean">
    {% for thesis in thesis_items %}
      <li>
        <strong>{{ thesis.title }}</strong>, {{ thesis.degree }}, {{ thesis.institution }}, {{ thesis.year }}.
        {% if thesis.advisor %}Advisor: {{ thesis.advisor }}.{% endif %}
        {% if thesis.description %} {{ thesis.description }}{% endif %}
        {% if thesis.pdf %} <a href="{{ thesis.pdf }}">PDF</a>{% endif %}
      </li>
    {% endfor %}
  </ul>
</section>

<section class="section-block">
  <h2>Full bibliography</h2>
  <div class="bibliography">
    {% bibliography %}
  </div>
</section>

<script>
  (function () {
    var select = document.getElementById("publication-year-filter");
    var items = Array.prototype.slice.call(document.querySelectorAll(".js-publication-item"));
    var empty = document.getElementById("publication-empty");

    function applyFilter() {
      var minYear = select.value ? parseInt(select.value, 10) : null;
      var visibleCount = 0;

      items.forEach(function (item) {
        var year = parseInt(item.getAttribute("data-year"), 10);
        var visible = !minYear || year >= minYear;
        item.hidden = !visible;
        if (visible) {
          visibleCount += 1;
        }
      });

      empty.hidden = visibleCount !== 0;
    }

    select.addEventListener("change", applyFilter);
    applyFilter();
  }());
</script>
