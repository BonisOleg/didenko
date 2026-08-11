"""Метрики сторінки «Про мене» — defaults, нормалізація, міграція з HTML body."""

from __future__ import annotations

import html
import re
from typing import Any

DEFAULT_ABOUT_METRICS: list[dict[str, str]] = [
    {
        'value': '100',
        'suffix': '%',
        'label': 'Дотримання законодавства України',
    },
    {
        'value': '3',
        'suffix': '+',
        'label': 'Етапів повного супроводу «під ключ»',
    },
    {
        'value': '100',
        'suffix': '%',
        'label': 'Конфіденційність та захист даних',
    },
    {
        'value': '40',
        'suffix': '+',
        'label': 'Відкритих проваджень у різних регіонах України',
    },
]

_STAT_BLOCK_RE = re.compile(
    r'<div\s+class="about-stat">(.*?)</div>',
    re.IGNORECASE | re.DOTALL,
)
_DATA_COUNT_RE = re.compile(r'data-count="(\d+)"', re.IGNORECASE)
_DATA_SUFFIX_RE = re.compile(r'data-suffix="([^"]*)"', re.IGNORECASE)
_LABEL_RE = re.compile(
    r'class="about-stat__label"[^>]*>([^<]*)',
    re.IGNORECASE,
)


def normalize_metrics(raw: Any) -> list[dict[str, str]]:
    """Повертає список {value, suffix, label}; value — ціле як рядок."""
    if not isinstance(raw, list):
        return []
    items: list[dict[str, str]] = []
    for row in raw:
        if not isinstance(row, dict):
            continue
        value_raw = str(row.get('value') or '').strip()
        if not value_raw.isdigit():
            continue
        label = html.unescape(str(row.get('label') or '').strip())
        if not label:
            continue
        suffix = str(row.get('suffix') or '').strip()
        items.append({'value': str(int(value_raw)), 'suffix': suffix, 'label': label})
    return items


def extract_metrics_from_body(body: str) -> list[dict[str, str]]:
    """Витягує метрики з legacy HTML у body (якщо є)."""
    if not body or 'about-stat' not in body:
        return []
    items: list[dict[str, str]] = []
    for match in _STAT_BLOCK_RE.finditer(body):
        block = match.group(1)
        count_m = _DATA_COUNT_RE.search(block)
        label_m = _LABEL_RE.search(block)
        if not count_m or not label_m:
            continue
        suffix_m = _DATA_SUFFIX_RE.search(block)
        items.append(
            {
                'value': count_m.group(1),
                'suffix': suffix_m.group(1) if suffix_m else '',
                'label': label_m.group(1).strip(),
            }
        )
    return normalize_metrics(items)


def strip_metrics_from_body(body: str) -> str:
    """Прибирає блок #about-metrics / .about-stats з HTML body."""
    if not body:
        return ''
    if 'about-metrics' not in body and 'about-stats' not in body:
        return body

    start_markers = (
        '<div class="about-stats" id="about-metrics"',
        "<div class=\"about-stats\" id='about-metrics'",
        '<div id="about-metrics"',
        "<div id='about-metrics'",
        '<div class="about-stats"',
    )
    start = -1
    for marker in start_markers:
        idx = body.find(marker)
        if idx != -1 and (start == -1 or idx < start):
            start = idx
    if start == -1:
        return body

    # Зріз від початку тега до закриття кореневого div (лічильник глибини).
    i = body.find('<', start)
    if i == -1:
        return body
    depth = 0
    pos = i
    end = -1
    while pos < len(body):
        if body.startswith('</div>', pos):
            depth -= 1
            pos += 6
            if depth == 0:
                end = pos
                break
            continue
        if body.startswith('<div', pos):
            # <div ...> або <div.../>
            gt = body.find('>', pos)
            if gt == -1:
                break
            if body[gt - 1] != '/':
                depth += 1
            pos = gt + 1
            continue
        pos += 1

    if end == -1:
        return body

    before = body[:start].rstrip()
    after = body[end:].lstrip()
    if before and after:
        return f'{before}\n\n{after}'
    return before or after


def insert_metrics_after_lead(body: str, metrics_html: str) -> str:
    """Вставляє HTML метрик після .about-lead; інакше — на початок."""
    if not metrics_html:
        return body
    if not body:
        return metrics_html

    lead_start = body.find('class="about-lead"')
    if lead_start == -1:
        lead_start = body.find("class='about-lead'")
    if lead_start == -1:
        return f'{metrics_html}\n{body}'

    tag_start = body.rfind('<', 0, lead_start)
    if tag_start == -1:
        return f'{metrics_html}\n{body}'

    depth = 0
    pos = tag_start
    end = -1
    while pos < len(body):
        if body.startswith('</div>', pos):
            depth -= 1
            pos += 6
            if depth == 0:
                end = pos
                break
            continue
        if body.startswith('<div', pos):
            gt = body.find('>', pos)
            if gt == -1:
                break
            if body[gt - 1] != '/':
                depth += 1
            pos = gt + 1
            continue
        pos += 1

    if end == -1:
        return f'{body}\n{metrics_html}'

    before = body[:end].rstrip()
    after = body[end:].lstrip()
    if after:
        return f'{before}\n\n{metrics_html}\n\n{after}'
    return f'{before}\n\n{metrics_html}'
