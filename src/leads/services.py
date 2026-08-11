"""Write-layer for leads: create + best-effort notify/CRM."""

from __future__ import annotations

import logging

import requests
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from src.leads.mail import resolve_lead_notify_email, send_lead_email
from src.leads.models import Lead

logger = logging.getLogger('src.leads')


def submit_lead(
    *,
    name: str,
    phone: str,
    email: str,
    consent: bool,
    source: str,
    source_url: str = '',
    service=None,
    selected_topics: list | None = None,
) -> Lead:
    if not consent:
        raise ValueError('consent required')

    with transaction.atomic():
        lead = Lead.objects.create(
            name=name,
            phone=phone,
            email=email,
            consent=True,
            source=source,
            source_url=source_url[:512],
            service=service,
            selected_topics=list(selected_topics or []),
            status=Lead.Status.NEW,
            is_read=False,
        )

    try:
        notify_lead(lead)
    except Exception:
        logger.exception('notify_lead failed for lead=%s', lead.pk)

    try:
        sync_lead_to_crm(lead)
    except Exception:
        logger.exception('sync_lead_to_crm failed for lead=%s', lead.pk)

    return lead


def _format_selected_topics(lead: Lead) -> str:
    topics = lead.selected_topics or []
    if not topics:
        return '—'
    return '\n'.join(f'- {topic}' for topic in topics)


def notify_lead(lead: Lead) -> None:
    subject = f'Нова заявка: {lead.name}'
    service_label = str(lead.service) if lead.service_id else '—'
    body = (
        f'Імʼя: {lead.name}\n'
        f'Телефон: {lead.phone}\n'
        f'Email: {lead.email}\n'
        f'Джерело: {lead.source}\n'
        f'URL: {lead.source_url}\n'
        f'Послуга: {service_label}\n'
        f'Користувач обрав такі поля:\n{_format_selected_topics(lead)}\n'
    )

    notify_to = resolve_lead_notify_email()
    if notify_to:
        send_lead_email(subject=subject, body=body, to_email=notify_to)

    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if token and chat_id:
        requests.post(
            f'https://api.telegram.org/bot{token}/sendMessage',
            json={'chat_id': chat_id, 'text': f'{subject}\n{body}'},
            timeout=10,
        )


def sync_lead_to_crm(lead: Lead) -> None:
    url = settings.CRM_WEBHOOK_URL
    if not url:
        return

    headers = {'Content-Type': 'application/json'}
    if settings.CRM_API_KEY:
        headers['Authorization'] = f'Bearer {settings.CRM_API_KEY}'

    payload = {
        'name': lead.name,
        'phone': lead.phone,
        'email': lead.email,
        'status': 'Новий лід',
        'source': lead.source,
        'source_url': lead.source_url,
        'service_id': lead.service_id,
        'selected_topics': lead.selected_topics or [],
        'internal_id': lead.pk,
    }
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()
    data = {}
    try:
        data = response.json()
    except ValueError:
        data = {}

    external_id = str(data.get('id') or data.get('external_id') or '')
    Lead.objects.filter(pk=lead.pk).update(
        crm_external_id=external_id[:64],
        crm_synced_at=timezone.now(),
    )
