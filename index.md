---
layout: default
title: Home
---
{% assign profile = site.data.profile %}
{% assign links = site.data.links %}

<section class="hero">
  <div>
    <h1>{{ profile.name }}</h1>
    <p class="lede">{{ profile.title }}</p>
    <p>{{ profile.bio_short }}</p>
    <div class="hero-meta">
      {% for affiliation in profile.affiliations %}
        <div>{{ affiliation }}</div>
      {% endfor %}
      <div>{{ profile.location }}</div>
    </div>
    <ul class="tag-list">
      {% for interest in profile.research_interests %}
        <li>{{ interest }}</li>
      {% endfor %}
    </ul>
    <div class="section-block">
      <div class="link-list">
        <a href="{{ '/publications/' | relative_url }}">View publications</a>
        <a href="{{ links.cv | relative_url }}">Download CV</a>
        <a href="{{ '/contact/' | relative_url }}">Contact</a>
      </div>
    </div>
  </div>
  <div class="hero-photo">
    <img src="{{ profile.photo | relative_url }}" alt="Portrait placeholder for {{ profile.name }}">
  </div>
</section>

<section class="section-block">
  <h2>Research agenda</h2>
  <p>
    This website focuses on research problems rather than a paper list alone. The aim is to develop AI systems
    that can operate in clinical and embodied settings where data are multimodal, decisions are high stakes,
    and deployment constraints matter as much as benchmark performance.
  </p>
  <div class="agenda-grid">
    {% for item in profile.research_agenda %}
      <article class="info-card">
        <h3>{{ item.title }}</h3>
        <p>{{ item.text }}</p>
      </article>
    {% endfor %}
  </div>
</section>

<section class="section-block">
  <h2>Selected directions</h2>
  <div class="card-grid">
    <article class="info-card">
      <h3>AI for medical imaging</h3>
      <p>Learning from heterogeneous image sources with limited annotation, shift-aware evaluation, and clinically grounded targets.</p>
    </article>
    <article class="info-card">
      <h3>Vision-language systems</h3>
      <p>Designing multimodal models that connect visual evidence, reports, and structured medical context.</p>
    </article>
    <article class="info-card">
      <h3>Robotics in healthcare</h3>
      <p>Integrating perception and planning for assistive and interventional robotic workflows.</p>
    </article>
    <article class="info-card">
      <h3>Reliable deployment</h3>
      <p>Improving calibration, uncertainty estimation, and evaluation protocols for real-world use.</p>
    </article>
  </div>
</section>

<section class="section-block">
  <h2>Current affiliations</h2>
  <ul class="list-clean">
    {% for affiliation in profile.affiliations %}
      <li>{{ affiliation }}</li>
    {% endfor %}
  </ul>
</section>
