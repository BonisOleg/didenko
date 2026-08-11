from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_sitesettings_blog_fonts'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='work_hours',
            field=models.CharField(
                blank=True,
                default='пн–пт з 9:00 до 18:00',
                max_length=120,
                verbose_name='Графік роботи',
            ),
        ),
    ]
