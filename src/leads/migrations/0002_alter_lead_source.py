# Generated manually for Lead.Source.BLOG

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='source',
            field=models.CharField(
                choices=[
                    ('home', 'Головна'),
                    ('hero', 'Hero'),
                    ('service', 'Послуга'),
                    ('contacts', 'Контакти'),
                    ('blog', 'Блог'),
                ],
                default='home',
                max_length=32,
                verbose_name='Джерело',
            ),
        ),
    ]
