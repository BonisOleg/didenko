"""Збірка HTML контенту «Про мене» з метриками після lead."""

from __future__ import annotations

from django.template.loader import render_to_string
from django.utils.safestring import SafeString, mark_safe

from src.pages.about_metrics import insert_metrics_after_lead, strip_metrics_from_body


def render_about_body_html(page) -> SafeString:
    """body без legacy-метрик + partial метрик після .about-lead."""
    body = strip_metrics_from_body(page.body or '')
    metrics = page.normalized_metrics()
    metrics_html = ''
    if metrics:
        metrics_html = render_to_string(
            'pages/partials/about_metrics.html',
            {'metrics': metrics},
        ).strip()
    return mark_safe(insert_metrics_after_lead(body, metrics_html))
