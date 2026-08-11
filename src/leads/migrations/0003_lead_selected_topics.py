from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_alter_lead_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='selected_topics',
            field=models.JSONField(
                blank=True,
                default=list,
                help_text='Пункти з блоку «Для кого», які обрав користувач.',
                verbose_name='Обрані теми',
            ),
        ),
    ]
