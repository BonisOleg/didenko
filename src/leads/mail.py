"""Email delivery for lead notifications (Resend or Django EMAIL_BACKEND)."""

from __future__ import annotations

import logging

import requests
from django.conf import settings
from django.core.mail import send_mail

from src.pages.models import SiteSettings

logger = logging.getLogger('src.leads')


def resolve_lead_notify_email() -> str:
    """Адмінське поле → fallback на ADMIN_NOTIFY_EMAIL з env."""
    site = SiteSettings.load()
    admin_email = (site.lead_notify_email or '').strip()
    if admin_email:
        return admin_email
    return (settings.ADMIN_NOTIFY_EMAIL or '').strip()


def send_lead_email(*, subject: str, body: str, to_email: str) -> None:
    """
    Якщо є RESEND_API_KEY — відправка через Resend API.
    Інакше — Django EMAIL_BACKEND (develop: console, production: SMTP).
    """
    to_email = (to_email or '').strip()
    if not to_email:
        logger.warning('lead email skipped: empty recipient')
        return

    api_key = (settings.RESEND_API_KEY or '').strip()
    if api_key:
        _send_via_resend(subject=subject, body=body, to_email=to_email, api_key=api_key)
        return

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=False,
    )


def _send_via_resend(
    *,
    subject: str,
    body: str,
    to_email: str,
    api_key: str,
) -> None:
    response = requests.post(
        settings.RESEND_API_URL,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
        json={
            'from': settings.DEFAULT_FROM_EMAIL,
            'to': [to_email],
            'subject': subject,
            'text': body,
        },
        timeout=15,
    )
    if response.status_code >= 400:
        logger.error(
            'Resend error status=%s body=%s',
            response.status_code,
            response.text[:500],
        )
    response.raise_for_status()
