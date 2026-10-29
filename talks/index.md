---
layout: page
title: Talks
permalink: /talks/
---

Research presentations and accompanying slides.

{% for talk in site.data.talks %}
## [{{ talk.title }}]({{ talk.url | relative_url }})

{% if talk.image %}
<a href="{{ talk.url | relative_url }}"><img src="{{ talk.image | relative_url }}" alt="{{ talk.image_alt | escape }}" width="360" height="360" loading="lazy" style="display:block;max-width:100%;height:auto;margin:1rem 0;"></a>
{% endif %}

{{ talk.subtitle }}

{{ talk.event }} · {{ talk.date | date: "%d %B %Y" }}

[Open presentation]({{ talk.url | relative_url }}) · [Main PDF]({{ talk.pdf }}) · [PDF with Q&A]({{ talk.full_pdf }})

<p><small><a href="{{ talk.update_url }}">Update / deployment status</a></small></p>
{% endfor %}
