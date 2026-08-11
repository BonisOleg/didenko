# Діденко — структура Django apps

Джерела: `Technical_Specification_Діденко.docx` · `DidenkoSitemap.pdf` · доповнення (Валерія Діденко) · референс hero (тип Звільнимо, адаптовано).  
Стек: Django 5+ · HTMX · HTML/CSS/JS · `project_structure` + `cooperative_design` (Prometey vault).  
Один репозиторій / один Django-проєкт. Google Ads / GTM — не окремий проєкт.

```
didenko/
  config/
  src/
    core/
    pages/
    services/
    blog/
    leads/
    seo/
  templates/
  static/
  media/
  deploy/
```

---

## `src.core` — shared kernel

- Mixins: `TimeStampedModel`, `SeoFieldsMixin` (title, description, h1)
- `SiteSettings` (singleton): телефон, email, адреса, координати карти, соцмережі
- Context processor → шапка / футер
- Templatetags, 404/500
- Без бізнес-моделей контенту

---

## `src.pages` — інфо-сторінки + головна

**URL:** `/` · `/pro-nas/` · `/kontakty/` · `/polityka-konfidentsiynosti/`

### Моделі

| Модель | Призначення |
|--------|-------------|
| `Page` | Інфо-сторінки (про мене, контакти, політика) + SEO |
| `HomeHero` | Singleton блок hero на `/` |
| `HomeBlock` | Інші секції головної: послуги-превʼю, переваги («чому»), «для кого», CTA |

### `HomeHero` — контракт (зафіксовано)

| Поле | Вимога |
|------|--------|
| `headline` | H1: «Банкрутство фізичних осіб під ключ» |
| `subheadline` | Короткий підтримуючий текст з доповнення (законне списання / Кодекс) |
| `image` | Плейсхолдер до готовності фото; **aspect-ratio 21:9** (full-bleed фон) |
| `image_alt` | Опис для a11y / SEO |
| `cta_label` | Напр. «Залишити заявку» / «Отримати консультацію» |
| `cta_target` | Якір/модалка форми ліда (`leads`) — **не квіз** |
| Overlay UI | Лише текст + одна CTA-група на hero; **без** віджета «реальні ситуації / кейси» |

Поведінка UI:

- Full-bleed hero (edge-to-edge), співвідношення **21:9**
- Sticky header окремо (`templates/partials/header.html`)
- CTA відкриває/скролить до форми з ТЗ §4.1: імʼя, телефон, email, чекбокс GDPR → AJAX → «Дякуємо за заявку»
- Блок кейсів у hero **не реалізовувати** (рішення 2026-07-28)

### `HomeBlock` — типи (після hero)

- `services_teaser` — превʼю послуг → `/posluhy/`
- `advantages` — «Чому звертаються» (з доповнення)
- `audience` — «Для кого» (з доповнення)
- `blog_teaser` — останні записи з `blog` (нижче fold, не в hero)
- `lead_form` — секція форми (якщо не в модалці)

---

## `src.services` — каталог послуг

**URL:** `/posluhy/` · `/posluhy/{slug}/`

| Модель | Призначення |
|--------|-------------|
| `Service` | slug, назва, опис, порядок, SEO, CTA → форма ліда з prefill послуги |

Seed (доповнення):

1. Консультації щодо процедури банкрутства ФО  
2. Аналіз фінансового стану та перспектив справи  
3. Підготовка документів для звернення до суду  
4. Повний супровід процедури неплатоспроможності  
5. Представництво інтересів під час судового розгляду  
6. Взаємодія з кредиторами та учасниками провадження  

---

## `src.blog` — кейси / новини (один розділ)

**URL:** `/blog/` · `/blog/{slug}/`

| Модель | Призначення |
|--------|-------------|
| `Category` | кейси / новини |
| `Post` | контент, дата, категорія, SEO, share URL |

HTMX-фільтр категорій на лістингу.  
На головну в hero **не** виводити; опційно `HomeBlock.blog_teaser` нижче.

---

## `src.leads` — заявки

| Модель | Призначення |
|--------|-------------|
| `Lead` | name, phone, email, consent, source_url, service FK (nullable), status=`new` |

- Views: HTMX/AJAX POST (головна, послуга, контакти)
- Signals/services: email адміна, Telegram (якщо ключі), CRM webhook (M5, після доступів)
- Валідація некоректних даних (ТЗ §6)

---

## `src.seo`

- `/sitemap.xml`, `/robots.txt`
- Хелпери canonical / meta з `SeoFieldsMixin`
- Без окремої polymorphic SEO-таблиці

---

## `INSTALLED_APPS` (порядок)

```python
INSTALLED_APPS = [
    # …
    "src.core",
    "src.pages",
    "src.services",
    "src.blog",
    "src.leads",
    "src.seo",
]
```

Адмін-сайдбар дзеркалить карту сайту (не назви apps): Головна/блоки → Про мене → Послуги → Блог → Контакти → Ліди → SEO → Налаштування.

---

## Поза Django-кодом

- GTM / GA4 / конверсії форм і `tel:`/`mailto:` — env + base template  
- Google Ads (ТЗ §7) — кабінет Ads, не app  

---

## Рішення (зафіксовано)

| # | Рішення |
|---|---------|
| 1 | Лише структура apps (цей файл); sitemap PDF / верстка — окремо |
| 2 | H1 hero = «Банкрутство фізичних осіб під ключ» |
| 3 | Віджет «реальні ситуації» у hero — **ні** |
| 4 | CTA = форма з ТЗ (не квіз) |
| 5 | Фото — плейсхолдер, **21:9** |
