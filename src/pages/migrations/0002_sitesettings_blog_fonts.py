from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='body_font',
            field=models.CharField(
                choices=[
                    ('inter', 'Inter'),
                    ('plus_jakarta', 'Plus Jakarta Sans'),
                    ('system', 'Системний'),
                ],
                default='inter',
                max_length=32,
                verbose_name='Шрифт тексту',
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='blog_author_name',
            field=models.CharField(
                blank=True,
                default='Діденко Валерія Валеріївна',
                max_length=120,
                verbose_name='Автор у блозі',
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='blog_cta_button',
            field=models.CharField(
                blank=True,
                default='Залишити заявку',
                max_length=80,
                verbose_name='Блог CTA кнопка',
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='blog_cta_text',
            field=models.TextField(
                blank=True,
                default=(
                    'Оціню вашу ситуацію та запропоную оптимальний правовий шлях '
                    'у межах Кодексу України з процедур банкрутства.'
                ),
                verbose_name='Блог CTA текст',
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='blog_cta_title',
            field=models.CharField(
                blank=True,
                default='Потрібна консультація?',
                max_length=120,
                verbose_name='Блог CTA заголовок',
            ),
        ),
    ]
