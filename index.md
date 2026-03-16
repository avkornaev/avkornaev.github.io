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
    <p>
      Alexei Kornaev works on machine learning and computer vision for scientific and clinical settings,
      with a focus on medical imaging, radiogenomics, trustworthy AI, physics-informed learning,
      and robotics. His research combines method development with questions of uncertainty,
      robustness, interpretability, and deployment in high-stakes environments.
    </p>
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
    The central theme of this work is reliable machine learning where physical constraints,
    medical context, and real-world variability matter. This includes uncertainty-aware prediction,
    physics-informed modeling, multimodal analysis of imaging and molecular data, and perception-action
    pipelines for embodied systems.
  </p>
  <div class="agenda-grid">
    <article class="info-card">
      <h3>Trustworthy and uncertainty-aware ML</h3>
      <p>Calibration, uncertainty estimation, failure analysis, and robust evaluation for high-stakes prediction tasks.</p>
    </article>
    <article class="info-card">
      <h3>Physics-informed learning</h3>
      <p>Neural and variational methods for scientific computing, inverse problems, and flow modeling in complex physical systems.</p>
    </article>
    <article class="info-card">
      <h3>Medical AI and radiogenomics</h3>
      <p>Joint analysis of medical imaging, pathology, molecular information, and clinical context for diagnosis and prognosis.</p>
    </article>
    <article class="info-card">
      <h3>Robotics and embodied AI</h3>
      <p>Perception, planning, and vision-language-action systems for robotic assistance and interactive environments.</p>
    </article>
  </div>
</section>

<section class="section-block">
  <h2>Selected directions</h2>
  <div class="card-grid">
    <article class="info-card">
      <h3>Medical imaging and multimodal diagnosis</h3>
      <p>Deep learning for radiology, pathology, and related multimodal pipelines that connect image evidence with clinical and biological context.</p>
    </article>
    <article class="info-card">
      <h3>PINNs and scientific machine learning</h3>
      <p>Physics-informed neural networks, neural surrogates, and variational formulations for computational mechanics and fluid-flow problems.</p>
    </article>
    <article class="info-card">
      <h3>Reliable AI in practice</h3>
      <p>Generalization under shift, uncertainty quantification, reproducibility, and evaluation protocols for deployment-oriented ML.</p>
    </article>
    <article class="info-card">
      <h3>Vision, language, and action</h3>
      <p>Multimodal systems that connect perception with reasoning and control in robotics and interactive AI settings.</p>
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
