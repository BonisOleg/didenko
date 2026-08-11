from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_featured',
            field=models.BooleanField(default=False, verbose_name='Головний кейс'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(
                fields=['is_featured', '-published_at'],
                name='blog_post_is_feat_7c2a1e_idx',
            ),
        ),
    ]
