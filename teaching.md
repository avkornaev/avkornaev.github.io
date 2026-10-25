---
title: Teaching
permalink: /teaching/
intro: Teaching in machine learning, computer vision, medical AI, and related computational methods.
---
## Course areas

- **Computer Vision**  
  Lecture-based and practical materials on image formation, feature learning, convolutional and transformer models, segmentation, and generative methods.
- **Machine Learning and Deep Learning**  
  Core methods for supervised learning, optimization, representation learning, and model evaluation.
- **Medical AI**  
  Topics in medical image analysis, multimodal clinical data, reliability, and deployment-oriented evaluation.
- **AI for Robotics and Embodied Systems**  
  Perception, control, planning, and multimodal reasoning for interactive systems.

## Course materials

{% assign ml_course = site.data.courses.courses | where: "id", "intro-to-ml-2026" | first %}
<article class="info-card teaching-course-card">
  <a href="{{ ml_course.links.course_site }}" aria-label="{{ ml_course.title }} — course website">
    <img src="{{ ml_course.image | relative_url }}" alt="{{ ml_course.image_alt }}" width="160" height="160" loading="lazy">
  </a>
  <div>
    <h3><a href="{{ ml_course.links.course_site }}">{{ ml_course.title }} · {{ ml_course.years | join: ", " }}</a></h3>
    <p>{{ ml_course.summary }}</p>
    <p><a href="{{ ml_course.links.course_site }}">Open course website →</a></p>
  </div>
</article>

- **Computer Vision 2026 LaTeX project**  
  Lecture sources, weekly PDFs, and notebooks are maintained in the repository under [the `teaching/cv-2026/` directory on GitHub](https://github.com/avkornaev/avkornaev.github.io/tree/main/teaching/cv-2026).

## Materials and format

- Slides and written lecture notes
- Practical notebooks and assignments
- Reading lists for selected topics
- Project-oriented materials for advanced courses

## Student supervision

- Supervision has included topics in medical imaging, trustworthy machine learning, scientific machine learning, and computer vision.
- Specific thesis titles, student names, and defended projects can be added here as they are finalized.
