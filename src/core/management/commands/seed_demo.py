from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from src.blog.models import Category, Post
from src.core.management.seed_about_body import ABOUT_BODY
from src.core.management.seed_about_hero import seed_pro_nas_hero_image
from src.core.management.seed_demo_images import seed_demo_images
from src.pages.about_metrics import DEFAULT_ABOUT_METRICS
from src.core.management.seed_services_data import SERVICES
from src.pages.models import HomeBlock, HomeHero, Page, SiteSettings
from src.services.models import Service


class Command(BaseCommand):
    help = 'Ідемпотентний seed демо-контенту Діденко'

    def handle(self, *args, **options):
        settings = SiteSettings.load()
        settings.phone = '+380994144849'
        settings.email = '3678802469@ukr.net'
        settings.address = 'Україна'
        settings.work_hours = 'пн–пт з 9:00 до 18:00'
        settings.map_embed_url = (
            'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d5080.73235292209'
            '!2d30.51162857654071!3d50.45290558718699!2m3!1f0!2f0!3f0!3m2!1i1024'
            '!2i768!4f13.1!3m3!1m2!1s0x40d4ce88e35e395f%3A0xc63774cf5da5a434'
            '!2z0KHQvtGE0ZbQudGB0YzQutC40Lkg0YHQvtCx0L7RgA!5e0!3m2!1suk!2sua'
            '!4v1785828669394!5m2!1suk!2sua'
        )
        settings.social_links = [
            {
                'label': 'Telegram',
                'url': 'https://t.me/+380994144849',
            },
            {
                'label': 'WhatsApp',
                'url': 'https://wa.me/380994144849',
            },
            {
                'label': 'Viber',
                'url': 'viber://chat?number=%2B380994144849',
            },
        ]
        settings.body_font = SiteSettings.BodyFont.INTER
        settings.blog_author_name = 'Діденко Валерія Валеріївна'
        settings.blog_cta_title = 'Потрібна консультація?'
        settings.blog_cta_text = (
            'Оціню вашу ситуацію та запропоную оптимальний правовий шлях '
            'у межах Кодексу України з процедур банкрутства.'
        )
        settings.blog_cta_button = 'Залишити заявку'
        settings.save()

        hero = HomeHero.load()
        hero.headline = (
            'Законне списання боргів та банкрутство фізичних осіб «під ключ»'
        )
        hero.subheadline = (
            'Допомагаю пройти процедуру неплатоспроможності відповідно до Кодексу '
            'України з процедур банкрутства та отримати можливість почати фінансове '
            'життя з чистого аркуша.'
        )
        hero.cta_label = 'Залишити заявку'
        hero.cta_target = '#lead-form'
        hero.image_alt = 'Арбітражна керуюча Діденко — плейсхолдер 21:9'
        hero.is_active = True
        hero.save()

        pages = [
            (
                'pro-nas',
                'Про мене',
                ABOUT_BODY,
                'Арбітражна керуюча Діденко Валерія Валеріївна',
                (
                    'Арбітражна керуюча Діденко Валерія Валеріївна — супровід процедур '
                    'неплатоспроможності фізичних осіб під ключ.'
                ),
            ),
            (
                'kontakty',
                'Контакти',
                '<p>Звʼяжіться для первинної консультації щодо процедури банкрутства.</p>',
                'Контакти',
                'Контакти арбітражної керуючої Діденко: телефон, email, форма заявки.',
            ),
            (
                'polityka-konfidentsiynosti',
                'Політика конфіденційності',
                (
                    '<p>Ми обробляємо персональні дані (імʼя, телефон, email) лише для '
                    'обробки заявок і звʼязку з вами відповідно до законодавства України.</p>'
                ),
                'Політика конфіденційності',
                'Політика обробки персональних даних сайту арбітражної керуючої Діденко.',
            ),
        ]
        for slug, title, body, seo_h1, seo_description in pages:
            defaults = {
                'title': title,
                'body': body,
                'is_published': True,
                'seo_h1': seo_h1,
                'seo_title': title,
                'seo_description': seo_description,
            }
            if slug == 'pro-nas':
                defaults['metrics'] = list(DEFAULT_ABOUT_METRICS)
            Page.objects.update_or_create(slug=slug, defaults=defaults)

        about_hero_status = seed_pro_nas_hero_image()
        self.stdout.write(f'about hero: {about_hero_status}')

        for i, item in enumerate(SERVICES, start=1):
            Service.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'title': item['title'],
                    'short_description': item['short'],
                    'body': item['body'],
                    'features': item['features'],
                    'deliverables': item['deliverables'],
                    'expected_result': item['expected_result'],
                    'timeline': item['timeline'],
                    'icon_key': item['icon_key'],
                    'sort_order': i,
                    'is_published': True,
                    'cta_label': 'Замовити послугу',
                },
            )

        keysy, _ = Category.objects.update_or_create(
            slug='keysy',
            defaults={
                'title': 'Реальні кейси',
                'sort_order': 1,
                'is_active': True,
            },
        )
        novyny, _ = Category.objects.update_or_create(
            slug='novyny',
            defaults={
                'title': 'Новини та законодавство',
                'sort_order': 2,
                'is_active': True,
            },
        )
        porady, _ = Category.objects.update_or_create(
            slug='porady',
            defaults={
                'title': 'Поради арбітражної керуючої',
                'sort_order': 3,
                'is_active': True,
            },
        )

        now = timezone.now()
        posts = [
            {
                'slug': 'keys-zakhyst-mayna',
                'category': keysy,
                'title': (
                    'Захист майна боржника під час виконавчого провадження '
                    'та скасування арештів'
                ),
                'excerpt': (
                    'Детальний розбір справи: як вдалося зупинити стягнення '
                    'з банківських рахунків, зберегти єдине житло та успішно '
                    'відкрити процедуру неплатоспроможності.'
                ),
                'is_featured': True,
                'days_ago': 13,
            },
            {
                'slug': 'keys-pryklad-1',
                'category': keysy,
                'title': (
                    'Приклад кейсу: списання кредитної заборгованості '
                    'понад 600 000 грн'
                ),
                'excerpt': (
                    'Комплексний супровід процедури неплатоспроможності '
                    'фізичної особи від подачі заяви до остаточного рішення суду.'
                ),
                'body': (
                    '<p>Комплексний супровід процедури неплатоспроможності '
                    'фізичної особи від подачі заяви до остаточного рішення суду.</p>'
                    '<p>Приклад кейсу: списання кредитної заборгованості '
                    'понад 600 000 грн — розбір від арбітражної керуючої '
                    'Діденко Валерії Валеріївни.</p>'
                ),
                'is_featured': False,
                'days_ago': 18,
            },
            {
                'slug': 'novyna-kodeks',
                'category': novyny,
                'title': (
                    'Оновлення судової практики за Кодексом '
                    'з процедур банкрутства'
                ),
                'excerpt': (
                    'Аналіз останніх правових позицій Верховного Суду щодо '
                    'реструктуризації боргів та відновлення платоспроможності.'
                ),
                'is_featured': False,
                'days_ago': 26,
            },
            {
                'slug': 'porada-pidhotovka-dokumentiv',
                'category': porady,
                'title': (
                    'Як підготувати документи для звернення до суду '
                    'про неплатоспроможність'
                ),
                'excerpt': (
                    'Практичний чекліст документів, типові помилки заявників '
                    'та як уникнути повернення заяви без розгляду.'
                ),
                'body': (
                    '<p>Практичний чекліст документів, типові помилки заявників '
                    'та як уникнути повернення заяви без розгляду.</p>'
                    '<p>Нижче — приклади матеріалів, з якими найчастіше працюємо '
                    'на етапі підготовки заяви.</p>'
                    '<p><img src="/static/img/about/docs-1.jpg" '
                    'alt="Підготовка комплекту документів" '
                    'width="960" height="540"></p>'
                    '<p><img src="/static/img/about/docs-2.jpg" '
                    'alt="Правові матеріали для звернення до суду" '
                    'width="960" height="540"></p>'
                    '<p>Якщо потрібна перевірка вашого комплекту — '
                    'залишіть заявку, і я підкажу наступні кроки.</p>'
                ),
                'is_featured': False,
                'days_ago': 30,
            },
            {
                'slug': 'keys-pryklad-2',
                'category': keysy,
                'title': 'Приклад кейсу: захист під час виконавчого провадження',
                'excerpt': (
                    'Алгоритм дій, коли вже відкрито виконавче провадження: '
                    'комунікація з виконавцем, арешти та підготовка до суду.'
                ),
                'is_featured': False,
                'days_ago': 40,
            },
        ]
        for item in posts:
            published_at = now - timedelta(days=item['days_ago'])
            body = item.get('body') or (
                f'<p>{item["excerpt"]}</p>'
                f'<p>{item["title"]} — розбір від арбітражної керуючої '
                f'Діденко Валерії Валеріївни.</p>'
            )
            Post.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'category': item['category'],
                    'title': item['title'],
                    'excerpt': item['excerpt'],
                    'body': body,
                    'is_published': True,
                    'is_featured': item['is_featured'],
                    'published_at': published_at,
                    'seo_h1': item['title'],
                    'seo_title': item['title'][:70],
                    'seo_description': item['excerpt'][:160],
                },
            )

        for line in seed_demo_images():
            self.stdout.write(f'images: {line}')

        blocks = [
            (
                HomeBlock.BlockType.AUDIENCE,
                'Вам потрібна допомога, якщо ви:',
                {
                    'intro': 'Сигнали, коли варто звернутися за супроводом процедури неплатоспроможності.',
                    'items': [
                        'Не можете своєчасно погашати кредити та позики.',
                        'Маєте значну заборгованість перед банками чи МФО.',
                        'Зіткнулися з виконавчими провадженнями, заблокованими картками чи арештом майна.',
                        'Шукаєте єдиний законний механізм повного врегулювання та списання боргів.',
                    ],
                },
                10,
            ),
            (
                HomeBlock.BlockType.SERVICES_TEASER,
                'Мої послуги',
                {'limit': 6},
                20,
            ),
            (
                HomeBlock.BlockType.ADVANTAGES,
                'Чому обирають мене',
                {
                    'intro': (
                        'Структурований супровід, прозорі умови та персональна '
                        'відповідальність на кожному етапі процедури.'
                    ),
                    'items': [
                        {
                            'title': 'Професійний юридичний супровід',
                            'text': (
                                'Практичний досвід у справах про неплатоспроможність '
                                'фізичних осіб та глибоке знання Кодексу України '
                                'з процедур банкрутства.'
                            ),
                        },
                        {
                            'title': 'Прозорі умови співпраці',
                            'text': (
                                'Чітко зафіксовані етапи, прозорий кошторис та жодних '
                                'прихованих платежів чи непередбачених комісій.'
                            ),
                        },
                        {
                            'title': 'Конфіденційність та відповідальність',
                            'text': (
                                'Повний захист вашої персональної та фінансової '
                                'інформації. Працюю виключно в межах чинного законодавства.'
                            ),
                        },
                        {
                            'title': 'Постійний звʼязок та підтримка',
                            'text': (
                                'Персональний супровід від первинної консультації '
                                'до прийняття судом остаточного рішення про списання боргів.'
                            ),
                        },
                    ],
                },
                30,
            ),
            (
                HomeBlock.BlockType.BLOG_TEASER,
                'Останні матеріали',
                {'limit': 3},
                40,
            ),
            (
                HomeBlock.BlockType.LEAD_FORM,
                'Залишити заявку',
                {'heading': 'Залишити заявку', 'anchor': 'lead-form'},
                50,
            ),
        ]
        for btype, title, payload, order in blocks:
            HomeBlock.objects.update_or_create(
                block_type=btype,
                defaults={
                    'title': title,
                    'payload': payload,
                    'sort_order': order,
                    'is_visible': True,
                },
            )

        keep_types = {btype for btype, *_ in blocks}
        HomeBlock.objects.exclude(block_type__in=keep_types).update(is_visible=False)

        self.stdout.write(self.style.SUCCESS('seed_demo OK'))
