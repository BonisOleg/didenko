from django.db import migrations


DEFAULT_CAPTION = 'Арбітражна керуюча • Практичний досвід'


def seed_pro_nas_caption(apps, schema_editor):
    Page = apps.get_model('pages', 'Page')
    Page.objects.filter(slug='pro-nas', hero_caption='').update(
        hero_caption=DEFAULT_CAPTION,
    )


def unseed_pro_nas_caption(apps, schema_editor):
    Page = apps.get_model('pages', 'Page')
    Page.objects.filter(slug='pro-nas', hero_caption=DEFAULT_CAPTION).update(
        hero_caption='',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_page_about_hero_image'),
    ]

    operations = [
        migrations.RunPython(seed_pro_nas_caption, unseed_pro_nas_caption),
    ]
