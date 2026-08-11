from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_page_about_hero_caption_seed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='map_embed_url',
            field=models.URLField(
                blank=True,
                default='',
                help_text=(
                    'Вставте код iframe з Google Maps (Поділитися → Вбудувати карту) '
                    'або прямий embed URL.'
                ),
                max_length=2048,
                verbose_name='Embed карти',
            ),
        ),
    ]
