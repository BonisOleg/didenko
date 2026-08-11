#!/usr/bin/env python3
"""Генерація DidenkoSitemap.pdf за Technical_Specification_Діденко.docx."""

from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT = Path(__file__).parent / "DidenkoSitemap.pdf"
VERSION = "1.0"
TZ_SOURCE = "Technical_Specification_Діденко.docx"

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

INK = colors.HexColor("#1A1A1A")
MUTED = colors.HexColor("#5A5550")
ACCENT = colors.HexColor("#1F3A5F")
ACCENT_2 = colors.HexColor("#2C5282")
HEADER_BG = colors.HexColor("#E8EEF5")
GRID = colors.HexColor("#C5CED9")
ROW_ALT = colors.HexColor("#F7F9FC")


def register_font() -> str:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            pdfmetrics.registerFont(TTFont("SiteFont", path))
            return "SiteFont"
    raise FileNotFoundError("Не знайдено шрифт із підтримкою кирилиці")


def p(text: str, style) -> Paragraph:
    return Paragraph(text.replace("\n", "<br/>"), style)


def build_styles(base_font: str):
    getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            fontName=base_font,
            fontSize=20,
            leading=26,
            alignment=TA_CENTER,
            spaceAfter=4,
            textColor=ACCENT,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            fontName=base_font,
            fontSize=10,
            leading=13,
            alignment=TA_CENTER,
            spaceAfter=12,
            textColor=MUTED,
        ),
        "h1": ParagraphStyle(
            "h1",
            fontName=base_font,
            fontSize=13,
            leading=17,
            spaceBefore=12,
            spaceAfter=6,
            textColor=ACCENT,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName=base_font,
            fontSize=11,
            leading=14,
            spaceBefore=8,
            spaceAfter=4,
            textColor=ACCENT_2,
        ),
        "body": ParagraphStyle(
            "body",
            fontName=base_font,
            fontSize=9,
            leading=12,
            spaceAfter=4,
            alignment=TA_LEFT,
            textColor=INK,
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName=base_font,
            fontSize=8,
            leading=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#888888"),
        ),
        "cell": ParagraphStyle(
            "cell",
            fontName=base_font,
            fontSize=8,
            leading=11,
            alignment=TA_LEFT,
            textColor=INK,
            wordWrap="CJK",
        ),
        "cell_header": ParagraphStyle(
            "cell_header",
            fontName=base_font,
            fontSize=8,
            leading=11,
            alignment=TA_LEFT,
            textColor=ACCENT,
            wordWrap="CJK",
        ),
    }


def _cell(text, style, header: bool = False) -> Paragraph:
    safe = (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    if header:
        safe = f"<b>{safe}</b>"
    return Paragraph(safe, style)


def tree_table(rows, col_widths, styles):
    wrapped = []
    for row_idx, row in enumerate(rows):
        wrapped_row = []
        for cell in row:
            style = styles["cell_header"] if row_idx == 0 else styles["cell"]
            if isinstance(cell, Paragraph):
                wrapped_row.append(cell)
            else:
                wrapped_row.append(_cell(cell, style, header=row_idx == 0))
        wrapped.append(wrapped_row)

    table = Table(wrapped, colWidths=col_widths, hAlign="LEFT", repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
                ("GRID", (0, 0), (-1, -1), 0.25, GRID),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW_ALT]),
            ]
        )
    )
    return table


def add_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("SiteFont", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(
        1.6 * cm,
        A4[1] - 1.1 * cm,
        "Діденко · DidenkoSitemap.pdf · на основі ТЗ · PrometeyLabs format",
    )
    canvas.drawRightString(A4[0] - 1.6 * cm, A4[1] - 1.1 * cm, f"v{VERSION}")
    canvas.drawCentredString(A4[0] / 2, 1.0 * cm, str(doc.page))
    canvas.restoreState()


def main():
    font = register_font()
    s = build_styles(font)
    today = date.today().isoformat()

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.6 * cm,
        title="Діденко — карта сайту",
        author="PrometeyLabs",
    )

    story = []

    story.append(p("КАРТА САЙТУ / SITEMAP", s["title"]))
    story.append(
        p(
            "Корпоративний сайт арбітражного керуючого «Діденко»",
            s["subtitle"],
        )
    )
    story.append(
        p(
            "Документ фіксує публічну карту URL, структуру адмін-панелі, інтеграції "
            "та критерії «ГОТОВО» за ТЗ. Формат узгоджений із базою знань Prometey "
            "(cooperative_design · seo_skill · референс notenhausSitemap / sitemapcommerce).",
            s["body"],
        )
    )
    story.append(
        p(
            f"Версія: {today} · v{VERSION} · Джерело: {TZ_SOURCE}<br/>"
            "Рішення: 1 розділ контенту (блог/кейси/новини) · шаблон послуг · "
            "/pro-nas/ · лише UA · юридичні сторінки за ТЗ §4.1",
            s["body"],
        )
    )
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 6))

    # 1. Метадані
    story.append(p("1. Метадані та статус рішень", s["h1"]))
    meta = [
        ["Параметр", "Статус / рішення"],
        ["Назва проєкту", "Діденко — корпоративний сайт арбітражного керуючого"],
        ["Мова", "UA (єдина; без /uk/ і без мовних дзеркал)"],
        ["URL-підхід", "ЧПУ UA-трансліт; lowercase + дефіси (seo_skill)"],
        ["Стек", "HTML/CSS/JS + HTMX · Python/Django (ТЗ §2.1)"],
        ["Адаптив", "320px → 1920px; sticky header (ТЗ §2.2, §3)"],
        ["Браузери", "Chrome, Safari, Firefox, Edge — останні версії (ТЗ §2.3)"],
        ["PageSpeed", "≥75 mobile / ≥90 desktop без сторонньої аналітики (ТЗ §2.4)"],
        ["SEO-база", "SSL · sitemap.xml · robots.txt · мета Title/Description/H1 (ТЗ §2.5)"],
        [
            "Критерій «ГОТОВО»",
            "Повний UX-сценарій без Fatal/404/500 + відповідність ТЗ + адаптив (ТЗ §1)",
        ],
        [
            "Контент-розділ",
            "Один розділ /blog/ — кейси + новини як категорії (узгоджено)",
        ],
    ]
    story.append(tree_table(meta, [4.2 * cm, 13.2 * cm], s))

    # 2. Публічний сайт
    story.append(p("2. Публічний сайт — карта URL", s["h1"]))
    story.append(
        p(
            "Кожен рядок нижче — обовʼязковий для sitemap-coverage verify "
            "(ecommerce_business_logic_skill / cooperative coverage). "
            "Службові маршрути — поза меню.",
            s["body"],
        )
    )
    public = [
        ["Розділ", "URL", "Примітка / критерій «ГОТОВО»"],
        [
            "Головна",
            "/",
            "Шапка (sticky), банер з УТП, блок послуг, переваги, "
            "превʼю блогу/кейсів; навігація працює (ТЗ §3)",
        ],
        [
            "Про мене",
            "/pro-nas/",
            "Історія, команда, сертифікати, метрики; фото масштабуються "
            "і відкриваються без помилок (ТЗ §3)",
        ],
        [
            "Послуги (список)",
            "/posluhy/",
            "Каталог послуг; клік відкриває внутрішню сторінку (ТЗ §3)",
        ],
        [
            "Послуга (шаблон)",
            "/posluhy/{slug}/",
            "Детальний опис; кнопки замовлення → форма заявки (ТЗ §3)",
        ],
        [
            "Блог / кейси / новини",
            "/blog/",
            "Єдиний розділ: стрічка + фільтр категорій (AJAX/HTMX без "
            "повного reload); пагінація; хронологія (ТЗ §3)",
        ],
        [
            "Запис блогу / кейс",
            "/blog/{slug}/",
            "Окрема стаття/кейс; кнопки «Поділитися» з коректним URL (ТЗ §3)",
        ],
        [
            "Контакти",
            "/kontakty/",
            "Адреса, tel:/mailto:, інтерактивна карта, форма ЗЗ (ТЗ §3)",
        ],
        [
            "Політика конфіденційності",
            "/polityka-konfidentsiynosti/",
            "Обовʼязково за ТЗ §4.1 (чекбокс згоди GDPR у всіх формах)",
        ],
        ["XML sitemap", "/sitemap.xml", "Автогенерація публічних URL (ТЗ §2.5)"],
        [
            "robots",
            "/robots.txt",
            "Disallow: /admin/; Sitemap: … (seo_skill)",
        ],
        ["Помилки", "404 / 500", "Шаблони помилок (системні)"],
    ]
    story.append(tree_table(public, [3.6 * cm, 4.4 * cm, 9.4 * cm], s))

    story.append(p("2.1. Глобальна шапка / підвал", s["h2"]))
    story.append(
        p(
            "<b>Header (sticky):</b> логотип → / · Про мене · Послуги · Блог · Контакти · CTA «Залишити заявку».<br/>"
            "<b>Footer:</b> навігація розділів · контакти · Політика конфіденційності · копірайт.",
            s["body"],
        )
    )

    story.append(p("2.2. Головна — блоки CMS (ТЗ §3)", s["h2"]))
    home = [
        ["Блок", "Зміст", "ГОТОВО"],
        ["Шапка", "Лого, меню, CTA", "Фіксується при скролі"],
        ["Hero / банер", "УТП арбітражного керуючого", "Коректне відображення 320–1920"],
        ["Послуги", "Перелік ключових послуг → /posluhy/{slug}/", "Кліки ведуть на внутрішні"],
        ["Переваги", "Ключові переваги / довіра", "Читабельно на mobile"],
        ["Блог / кейси", "Останні записи з /blog/", "Хронологія без 404"],
        ["Форма / CTA", "Імʼя, телефон, email + згода GDPR", "AJAX → «Дякуємо за заявку»"],
    ]
    story.append(tree_table(home, [3.2 * cm, 7.5 * cm, 6.7 * cm], s))

    story.append(p("2.3. Послуги — шаблон (ТЗ §3)", s["h2"]))
    story.append(
        p(
            "Багаторівневість реалізується через список `/posluhy/` і детальні сторінки "
            "`/posluhy/{slug}/` (конкретний перелік послуг — контент CMS, не жорстко в карті). "
            "На деталі: опис, CTA «Замовити» → модалка/якір форми з prefill послуги.",
            s["body"],
        )
    )

    story.append(p("2.4. Блог — єдиний контент-розділ (ТЗ §3)", s["h2"]))
    blog = [
        ["Елемент", "Поведінка"],
        ["Лістинг /blog/", "Картки записів; категорії (кейси / новини); пагінація"],
        ["Фільтр категорій", "HTMX/AJAX без повного перезавантаження сторінки"],
        ["Запис /blog/{slug}/", "Контент, медіа, дата; share-кнопки з absolute URL"],
        ["SEO", "Окремі Title / Description / H1 на кожен запис (ТЗ §5.2)"],
    ]
    story.append(tree_table(blog, [4.5 * cm, 12.9 * cm], s))

    story.append(PageBreak())

    # 3. Адмінка
    story.append(p("3. Адмін-панель — карта модулів (ТЗ §5)", s["h1"]))
    story.append(
        p(
            "Сайдбар дзеркалить структуру сайту (не Django apps). "
            "Стек CMS: Django admin / кастомна панель за cooperative_design.",
            s["body"],
        )
    )
    admin = [
        ["Модуль", "Зона", "Функції · критерій «ГОТОВО»"],
        [
            "Дашборд",
            "/admin/",
            "Огляд нових лідів, швидкі посилання",
        ],
        [
            "Інфо-сторінки",
            "контент",
            "Редагування /pro-nas/, /kontakty/, політики (ТЗ §5.1)",
        ],
        [
            "Блоки головної",
            "контент",
            "Hero, УТП, переваги — тексти/медіа без коду",
        ],
        [
            "Послуги",
            "каталог",
            "CRUD послуг: назва, slug, опис, порядок, SEO",
        ],
        [
            "Блог / кейси",
            "блог",
            "CRUD записів, категорії, публікація, пагінація на вітрині",
        ],
        [
            "SEO-модуль",
            "meta",
            "Title, Description, H1 для кожної сторінки/запису (ТЗ §5.2)",
        ],
        [
            "Ліди / заявки",
            "ліди",
            "Усі заявки у внутрішній БД; статус «Новий лід» (ТЗ §5.3)",
        ],
        [
            "Контакти сайту",
            "налаштування",
            "Телефони, email, адреса, координати карти",
        ],
        [
            "Інтеграції",
            "налаштування",
            "Ключі GA4/GTM/CRM/Telegram — лише через env, не в git",
        ],
    ]
    story.append(tree_table(admin, [3.4 * cm, 2.8 * cm, 11.2 * cm], s))

    # 4. Інтеграції та форми
    story.append(p("4. Інтеграції та форми (ТЗ §4)", s["h1"]))
    integ = [
        ["Сервіс", "Точки / маршрути", "Критерій «ГОТОВО»"],
        [
            "Форми ЗЗ",
            "POST AJAX (головна / послуга / контакти)",
            "Імʼя, телефон, email; чекбокс GDPR; «Дякуємо за заявку»; "
            "без reload; запис у CMS",
        ],
        [
            "Email адміна",
            "бекенд notify",
            "Лист на email адміністратора",
        ],
        [
            "Telegram-бот",
            "webhook / bot API",
            "Дубль заявки в Telegram (за наявності токена)",
        ],
        [
            "CRM",
            "Webhooks/API",
            "Лід зі статусом «Новий лід» (ТЗ §4.3); лише після надання доступів",
        ],
        [
            "GA4 + GTM",
            "контейнер у base",
            "Підключення за ID від Замовника (ТЗ §4.2, §7.1)",
        ],
        [
            "Конверсії",
            "події GTM/GA4",
            "Відправка форми; клік tel:/mailto: (ТЗ §7.1.3)",
        ],
    ]
    story.append(tree_table(integ, [3.2 * cm, 5.0 * cm, 9.2 * cm], s))
    story.append(
        p(
            "<b>Умова ТЗ §4.4:</b> зовнішні сервіси підключаються лише після своєчасного "
            "надання Замовником доступів, API-ключів і документації.",
            s["body"],
        )
    )

    # 5. Google Ads
    story.append(p("5. Google Ads — обсяг робіт (ТЗ §7)", s["h1"]))
    ads = [
        ["Блок", "Склад", "ГОТОВО"],
        [
            "Аналітика",
            "GTM + GA4 + цільові події",
            "Конверсії фіксуються в GA4",
        ],
        [
            "Кабінет",
            "Створення Ads + звʼязок з GA4",
            "Імпорт конверсій працює",
        ],
        [
            "Кампанія",
            "1 пошукова кампанія: семантика, мінус-слова, групи, розширення",
            "Пройшла модерацію, у показах",
        ],
        [
            "Ведення",
            "1 місяць моніторингу/оптимізації з моменту запуску",
            "Супровід виконано",
        ],
    ]
    story.append(tree_table(ads, [3.0 * cm, 8.5 * cm, 5.9 * cm], s))

    # 6. E2E
    story.append(p("6. E2E чек-лист ↔ URL (ТЗ §6)", s["h1"]))
    e2e = [
        ["№", "Тест-кейс", "URL / покриття"],
        ["1", "Відправка форми «Залишити заявку»", "/ · /posluhy/{slug}/ · /kontakty/"],
        ["2", "Некоректні дані — блокування + підказки", "усі форми"],
        ["3", "Мобільний вигляд + мобільне меню", "усі публічні"],
        ["4", "Навігація без битих посилань / 404", "уся карта §2"],
    ]
    story.append(tree_table(e2e, [1.0 * cm, 7.5 * cm, 8.9 * cm], s))

    story.append(PageBreak())

    # 7. Roadmap
    story.append(p("7. Модульний roadmap (ядро за ТЗ)", s["h1"]))
    road = [
        ["Фаза", "Склад", "Статус"],
        [
            "M0 Вітрина",
            "Шапка/footer sticky, головна, /pro-nas/, /posluhy/+/ {slug}/, "
            "/blog/+/ {slug}/ (фільтри HTMX), /kontakty/, політика",
            "Обовʼязково",
        ],
        [
            "M1 Ліди",
            "Форми AJAX + GDPR, email/Telegram, ліди в CMS",
            "Обовʼязково",
        ],
        [
            "M2 Адмінка",
            "CRUD контенту, послуг, блогу, SEO-мета, контакти",
            "Обовʼязково",
        ],
        [
            "M3 SEO/Perf",
            "sitemap.xml, robots, PageSpeed ≥75/90, SSL, ЧПУ",
            "Обовʼязково",
        ],
        [
            "M4 Аналітика+Ads",
            "GTM, GA4, конверсії, 1 пошукова кампанія + 1 міс. ведення",
            "Обовʼязково (ТЗ §7)",
        ],
        [
            "M5 CRM",
            "Webhook/API передача лідів — після доступів Замовника",
            "Умовно (§4.4)",
        ],
    ]
    story.append(tree_table(road, [2.6 * cm, 11.0 * cm, 3.8 * cm], s))

    # 8. Coverage
    story.append(p("8. Sitemap-coverage verify (шаблон здачі)", s["h1"]))
    story.append(
        p(
            "Заповнюється на етапі реалізації. Будь-який рядок без статусу — "
            "блокер приймання (ERR-BIZ-01).",
            s["body"],
        )
    )
    cov = [
        ["URL з карти", "urls", "View", "Шаблон", "Навігація", "Статус"],
        ["/", "☐", "☐", "☐", "☐", ""],
        ["/pro-nas/", "☐", "☐", "☐", "☐", ""],
        ["/posluhy/", "☐", "☐", "☐", "☐", ""],
        ["/posluhy/{slug}/", "☐", "☐", "☐", "☐", ""],
        ["/blog/", "☐", "☐", "☐", "☐", ""],
        ["/blog/{slug}/", "☐", "☐", "☐", "☐", ""],
        ["/kontakty/", "☐", "☐", "☐", "☐", ""],
        ["/polityka-konfidentsiynosti/", "☐", "☐", "☐", "☐", ""],
        ["/sitemap.xml", "☐", "☐", "—", "—", ""],
        ["/robots.txt", "☐", "☐", "—", "—", ""],
    ]
    story.append(
        tree_table(
            cov,
            [5.2 * cm, 1.8 * cm, 1.8 * cm, 2.2 * cm, 2.6 * cm, 3.8 * cm],
            s,
        )
    )

    story.append(Spacer(1, 10))
    story.append(
        p(
            f"Референс формату: notenhausSitemap.pdf · sitemapcommerce.pdf · "
            f"cooperative_design<br/>Документ: DidenkoSitemap.pdf · Версія: {today} v{VERSION}",
            s["footer"],
        )
    )

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"OK → {OUTPUT}")


if __name__ == "__main__":
    main()
