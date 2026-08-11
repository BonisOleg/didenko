"""Ідемпотентний seed SiteBlock з registry defaults."""

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand

from src.pages.block_defaults import BLOCK_CONTENT_TYPES, default_for_key
from src.pages.models_siteblock import SiteBlock
from src.pages.site_content_registry import all_registry_block_keys, label_for_block


class Command(BaseCommand):
    help = 'Seed SiteBlock keys from CMS registry (no overwrite of existing text/images).'

    def handle(self, *args, **options):
        created = 0
        for i, (page, key) in enumerate(all_registry_block_keys(), start=1):
            content_type = BLOCK_CONTENT_TYPES.get((page, key), 'text')
            _, was_created = SiteBlock.objects.get_or_create(
                page=page,
                key=key,
                defaults={
                    'label': label_for_block(page, key),
                    'text_html': default_for_key(page, key),
                    'content_type': content_type,
                    'sort_order': i,
                    'is_active': True,
                },
            )
            if was_created:
                created += 1
        cache.delete(getattr(settings, 'SITE_BLOCKS_CACHE_KEY', 'didenko_site_blocks_v1'))
        self.stdout.write(self.style.SUCCESS(f'SiteBlock seed: +{created} нових'))
