---
title: Publications
permalink: /publications/
intro: Publications are synced from ORCID into BibTeX and structured site data. By default this page shows the full all-years list, with optional filters for recent subsets, conference papers, and theses.
---
{% assign publication_items = site.data.publications.items | sort: "year" | reverse %}
{% assign thesis_items = site.data.theses | sort: "year" | reverse %}
{% assign conference_items = publication_items | where: "category", "conference" %}
{% assign thesis_publication_items = publication_items | where: "category", "thesis" %}
{% assign current_year = site.time | date: "%Y" | plus: 0 %}

<section class="section-block">
  <h2>Automatic sources</h2>
  <p class="muted-text">
    This site is configured to sync publications automatically from ORCID on a schedule. Google Scholar is kept as a manual reference because it does not provide a stable public API for this use case, while Scopus and Web of Science can be added later if API credentials are available.
  </p>
</section>

<section class="section-block">
  <h2>Filter publication lists</h2>
  <div class="filter-bar">
    <label for="publication-window-filter">Quick range:</label>
    <select id="publication-window-filter">
      <option value="" selected>All years</option>
      <option value="3">Last 3 years</option>
      <option value="5">Last 5 years</option>
      <option value="10">Last 10 years</option>
    </select>
    <label for="publication-year-filter">Or start from year:</label>
    <select id="publication-year-filter">
      <option value="" selected>All years</option>
      {% assign years = publication_items | map: "year" | uniq | sort | reverse %}
      {% for year in years %}
        <option value="{{ year }}">{{ year }} and later</option>
      {% endfor %}
    </select>
  </div>
</section>

<section class="section-block">
  <h2>Publication list</h2>
  <div id="publication-results">
    {% for item in publication_items %}
      {% unless item.category == "conference" or item.category == "thesis" %}
        <article class="publication-item js-filterable-item" data-year="{{ item.year }}" data-kind="publication">
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
    {% for item in conference_items %}
      <li class="js-filterable-item" data-year="{{ item.year }}" data-kind="conference">
        <strong>{{ item.title }}</strong>, {% if item.venue %}<em>{{ item.venue }}</em>, {% endif %}{{ item.year }}.
        {% if item.doi %}<a href="https://doi.org/{{ item.doi }}">DOI</a>{% endif %}
      </li>
    {% endfor %}
    {% if conference_items.size == 0 %}
      <li>Conference entries will appear here when available in ORCID or publication overrides.</li>
    {% endif %}
  </ul>
  <p id="conference-empty" class="muted-text" hidden>No conference papers match the selected year range.</p>
</section>

<section class="section-block">
  <h2>Theses</h2>
  <ul class="list-clean">
    {% for thesis in thesis_publication_items %}
      <li class="js-filterable-item" data-year="{{ thesis.year }}" data-kind="thesis">
        <strong>{{ thesis.title }}</strong>{% if thesis.venue %}, {{ thesis.venue }}{% endif %}, {{ thesis.year }}.
        {% if thesis.doi %}<a href="https://doi.org/{{ thesis.doi }}">DOI</a>{% endif %}
      </li>
    {% endfor %}
    {% for thesis in thesis_items %}
      <li class="js-filterable-item" data-year="{{ thesis.year }}" data-kind="thesis">
        <strong>{{ thesis.title }}</strong>, {{ thesis.degree }}, {{ thesis.institution }}, {{ thesis.year }}.
        {% if thesis.advisor %}Advisor: {{ thesis.advisor }}.{% endif %}
        {% if thesis.description %} {{ thesis.description }}{% endif %}
        {% if thesis.pdf %} <a href="{{ thesis.pdf }}">PDF</a>{% endif %}
      </li>
    {% endfor %}
  </ul>
  <p id="thesis-empty" class="muted-text" hidden>No theses match the selected year range.</p>
</section>

<section class="section-block">
  <h2>Full bibliography</h2>
  <div class="bibliography">
    {% bibliography %}
  </div>
</section>

<script>
  (function () {
    var currentYear = {{ current_year }};
    var windowSelect = document.getElementById("publication-window-filter");
    var select = document.getElementById("publication-year-filter");
    var items = Array.prototype.slice.call(document.querySelectorAll(".js-filterable-item"));
    var emptyPublications = document.getElementById("publication-empty");
    var emptyConferences = document.getElementById("conference-empty");
    var emptyTheses = document.getElementById("thesis-empty");

    function getMinYear() {
      if (windowSelect.value) {
        return currentYear - parseInt(windowSelect.value, 10) + 1;
      }
      if (select.value) {
        return parseInt(select.value, 10);
      }
      return null;
    }

    function applyFilter() {
      var minYear = getMinYear();
      var counts = {
        publication: 0,
        conference: 0,
        thesis: 0
      };

      items.forEach(function (item) {
        var year = parseInt(item.getAttribute("data-year"), 10);
        var kind = item.getAttribute("data-kind");
        var visible = !minYear || year >= minYear;
        item.hidden = !visible;
        if (visible) {
          counts[kind] += 1;
        }
      });

      emptyPublications.hidden = counts.publication !== 0;
      emptyConferences.hidden = counts.conference !== 0;
      emptyTheses.hidden = counts.thesis !== 0;
    }

    windowSelect.addEventListener("change", function () {
      if (windowSelect.value) {
        select.value = "";
      }
      applyFilter();
    });
    select.addEventListener("change", function () {
      if (select.value) {
        windowSelect.value = "";
      }
      applyFilter();
    });
    applyFilter();
  }());
</script>
