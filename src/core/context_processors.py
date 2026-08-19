import re

from django.conf import settings
from django.core.cache import cache

from src.leads.forms import LeadForm
from src.leads.models import Lead
from src.pages.favicon import get_favicon_urls
from src.pages.models import SiteSettings
from src.pages.models_theme import ActiveTheme

_TAG_ID_RE = re.compile(r'^[A-Z0-9-]+$')


def _clean_tag_id(value: str) -> str:
    value = (value or '').strip()
    return value if _TAG_ID_RE.fullmatch(value) else ''

SITE_BLOCKS_CACHE_KEY = 'didenko_site_blocks_v1'
SITE_BLOCKS_CACHE_TTL = 60


def _load_site_blocks() -> dict:
    blocks = cache.get(SITE_BLOCKS_CACHE_KEY)
    if blocks is None:
        from src.pages.models_siteblock import SiteBlock

        blocks = {
            b.cache_key: b
            for b in SiteBlock.objects.filter(is_active=True)
        }
        cache.set(SITE_BLOCKS_CACHE_KEY, blocks, SITE_BLOCKS_CACHE_TTL)
    return blocks


def site_context(request):
    try:
        site_settings = SiteSettings.load()
    except Exception:
        site_settings = None

    theme_version = 0
    try:
        theme = ActiveTheme.get_solo()
        if theme.updated_at:
            theme_version = int(theme.updated_at.timestamp())
    except Exception:
        theme = None

    return {
        'site_settings': site_settings,
        'site_blocks': _load_site_blocks(),
        'favicon_urls': get_favicon_urls(site_settings),
        'theme_version': theme_version,
        'lead_modal_form': LeadForm(source=Lead.Source.BLOG, prefix='modal'),
        'gtm_container_id': _clean_tag_id(settings.GTM_CONTAINER_ID),
        'google_tag_id': _clean_tag_id(settings.GOOGLE_TAG_ID)
        or _clean_tag_id(settings.GA4_MEASUREMENT_ID),
        'ga4_measurement_id': _clean_tag_id(settings.GA4_MEASUREMENT_ID),
    }
