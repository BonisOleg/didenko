import copy

from django.db import migrations, models

from src.pages.about_metrics import (
    DEFAULT_ABOUT_METRICS,
    extract_metrics_from_body,
    strip_metrics_from_body,
)


def seed_about_metrics(apps, schema_editor):
    Page = apps.get_model('pages', 'Page')
    for page in Page.objects.filter(slug='pro-nas'):
        extracted = extract_metrics_from_body(page.body or '')
        page.metrics = extracted or copy.deepcopy(DEFAULT_ABOUT_METRICS)
        page.body = strip_metrics_from_body(page.body or '')
        page.save(update_fields=['metrics', 'body', 'updated_at'])


def unseed_about_metrics(apps, schema_editor):
    Page = apps.get_model('pages', 'Page')
    Page.objects.filter(slug='pro-nas').update(metrics=[])


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_sitesettings_map_embed_url_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='metrics',
            field=models.JSONField(
                blank=True,
                default=list,
                help_text=(
                    'Лише для «Про мене» (pro-nas). Список: число, суфікс (% / +), підпис.'
                ),
                verbose_name='Ключові показники',
            ),
        ),
        migrations.RunPython(seed_about_metrics, unseed_about_metrics),
    ]
