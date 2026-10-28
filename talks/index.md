---
layout: page
title: Talks
permalink: /talks/
---

Research presentations and accompanying slides.

{% for talk in site.data.talks %}
## [{{ talk.title }}]({{ talk.url | relative_url }})

{{ talk.subtitle }}

{{ talk.event }} · {{ talk.date | date: "%d %B %Y" }}

[Open presentation]({{ talk.url | relative_url }}) · [Main PDF]({{ talk.pdf }}) · [PDF with Q&A]({{ talk.full_pdf }})

<p><small><a href="{{ talk.update_url }}">Update / deployment status</a></small></p>
{% endfor %}
