# Діденко — схема БД (tables.md)

**Версія:** 1.0 · **Дата:** 2026-07-28 · **Статус lock:** DRAFT→APPROVED (рішення клієнта)  
**Джерела:** `Technical_Specification_Діденко.docx` · `DidenkoSitemap.pdf` v1.0 · `apps_structure.md` · доповнення (Валерія Діденко)  
**Регламент:** Prometey `ecommerce_db_schema_skill` (процес verify) + `cooperative_design` + `seo_skill`  
**Стек:** Django 5+ · PostgreSQL · UA only · HTMX-форми · без e-commerce

---

## 0. Scratchpad / lock

| Тема | Рішення |
|---|---|
| Apps | `core` (mixins only) · `pages` · `services` · `blog` · `leads` · `seo` |
| Мова | UA only; без `*_en` / parler |
| SEO override | `seo_title` · `seo_description` · `seo_h1` на сутностях з публічним URL (ТЗ §2.5, §5.2) |
| Keywords | **немає** в ТЗ → колонки `seo_keywords` не створюємо |
| HomeBlock | **A:** рядок + `payload` JSONB |
| Про мене | **A:** лише `pages_page.body` (WYSIWYG); без team/certificate/metric таблиць |
| Lead поля | **A:** `name`, `phone`, `email`, `consent` (+ службові) |
| CRM M5 | **A:** `crm_external_id` hook одразу |
| Hero кейси | не в БД як окремий віджет; blog_teaser лише через HomeBlock type |
| Auth публічний | немає (адмін-only Django User) |
| Secrets | GA4/GTM/Telegram/CRM tokens — лише `.env`, не в таблицях |

`core` — shared kernel mixins (`TimeStampedModel`, `SeoFieldsMixin`), **не** app зі схеми таблиць (окрім якщо `SiteSettings` живе в `pages` — див. §3.1).

---

## 1. Apps ↔ таблиці

| App | Таблиці |
|---|---|
| `pages` | `pages_site_settings` · `pages_page` · `pages_home_hero` · `pages_home_block` |
| `services` | `services_service` |
| `blog` | `blog_category` · `blog_post` |
| `leads` | `leads_lead` |
| `seo` | `seo_redirect_301` (опційно M3; мінімум — код sitemap/robots без таблиць) |
| `core` | — (abstract mixins only) |

---

## 2. ER

```
pages_site_settings          (singleton)
pages_home_hero              (singleton)
pages_home_block             (N rows, typed + JSONB payload)
pages_page                   (про-нас / контакти / політика / інші)

services_service

blog_category ──── 1:M ──── blog_post

leads_lead ──── M:1 ──── services_service   (nullable FK)
leads_lead.crm_external_id                   (hook M5)

seo_redirect_301                               (опційно)
```

URL resolve:

| URL | Джерело |
|---|---|
| `/` | `pages_home_hero` + `pages_home_block` (+ teaser з `services` / `blog`) |
| `/pro-nas/` · `/kontakty/` · `/polityka-konfidentsiynosti/` | `pages_page.slug` |
| `/posluhy/` · `/posluhy/{slug}/` | `services_service` |
| `/blog/` · `/blog/{slug}/` | `blog_post` (+ filter `blog_category`) |
| `/sitemap.xml` · `/robots.txt` | код `seo` + публічні моделі |

---

## 3. Таблиці ядра (M0–M2)

Типи: `PK` bigserial · slug `varchar(160)` · timestamps `timestamptz` через mixin · ImageField → `varchar(512)` path.

### 3.0. Mixins (`core`, abstract — без таблиць)

**`TimeStampedModel`:** `created_at`, `updated_at`  
**`SeoFieldsMixin`:** `seo_title` varchar(70) NULL · `seo_description` varchar(160) NULL · `seo_h1` varchar(255) NULL

Fallback на вітрині: якщо SEO-поле порожнє → title/name сутності.

---

### 3.1. `pages_site_settings` (singleton)

| Колонка | Тип | Null | Примітка |
|---|---|---|---|
| id | PK | | завжди `id=1` (enforce в save/admin) |
| phone | varchar(32) | ✓ | `tel:` у шапці |
| email | varchar(254) | ✓ | `mailto:` |
| address | text | ✓ | контакти / футер |
| map_lat | numeric(9,6) | ✓ | інтерактивна карта |
| map_lng | numeric(9,6) | ✓ | |
| map_embed_url | varchar(512) | ✓ | альтернатива lat/lng |
| social_links | jsonb | ✓ | `[{label, url}]` |
| robots_extra | text | ✓ | доп. директиви (seo) |
| created_at / updated_at | | | |

---

### 3.2. `pages_page`

| Колонка | Тип | Null | Примітка |
|---|---|---|---|
| id | PK | | |
| slug | varchar(160) | | unique → `/pro-nas/`, `/kontakty/`, `/polityka-konfidentsiynosti/` |
| title | varchar(255) | | |
| body | text | | WYSIWYG HTML (команда/сертифікати/метрики — у контенті) |
| is_published | bool | | default true |
| seo_* | mixin | ✓ | |
| created_at / updated_at | | | |

Індекс: `(is_published, slug)`.  
Seed slug: `pro-nas`, `kontakty`, `polityka-konfidentsiynosti`.

---

### 3.3. `pages_home_hero` (singleton)

| Колонка | Тип | Null | Примітка |
|---|---|---|---|
| id | PK | | `id=1` |
| headline | varchar(255) | | H1: «Банкрутство фізичних осіб під ключ» |
| subheadline | text | ✓ | підтримуючий текст |
| image | varchar(512) | ✓ | плейсхолдер; UI **21:9** full-bleed |
| image_alt | varchar(255) | ✓ | |
| cta_label | varchar(120) | | напр. «Залишити заявку» |
| cta_target | varchar(64) | | `#lead-form` \| `modal:lead` (код) |
| is_active | bool | | default true |
| created_at / updated_at | | | |

Без віджета кейсів / «реальні ситуації».

---

### 3.4. `pages_home_block`

| Колонка | Тип | Null | Примітка |
|---|---|---|---|
| id | PK | | |
| block_type | varchar(32) | | див. enum нижче |
| title | varchar(255) | ✓ | заголовок секції |
| payload | jsonb | | структура залежить від `block_type` |
| sort_order | int | | default 0 |
| is_visible | bool | | default true |
| created_at / updated_at | | | |

**`block_type` enum (код):**

| type | Призначення payload (приклад) |
|---|---|
| `services_teaser` | `{ "limit": 6 }` — дані з `services_service` |
| `advantages` | `{ "items": [{ "title", "text", "icon?" }] }` — «Чому звертаються» |
| `audience` | `{ "intro?", "items": ["…"] }` — «Для кого» |
| `blog_teaser` | `{ "limit": 3, "category_slug?": "keysy" }` — з `blog_post` |
| `lead_form` | `{ "heading?", "anchor": "lead-form" }` — форма з ТЗ |

Check: `block_type IN (...)`. Індекс: `(is_visible, sort_order)`.

---

### 3.5. `services_service`

| Колонка | Тип | Null | Примітка |
|---|---|---|---|
| id | PK | | |
| slug | varchar(160) | | unique → `/posluhy/{slug}/` |
| title | varchar(255) | | |
| short_description | varchar(500) | ✓ | картка в лістингу / головна |
| body | text | | детальний опис |
| sort_order | int | | |
| is_published | bool | | |
| cta_label | varchar(120) | ✓ | default «Замовити» |
| seo_* | mixin | ✓ | |
| created_at / updated_at | | | |

Індекс: `(is_published, sort_order)`.  
Seed: 6 послуг з доповнення (див. `apps_structure.md`).

---

### 3.6. `blog_category`

| Колонка | Тип | Null | Примітка |
|---|---|---|---|
| id | PK | | |
| slug | varchar(160) | | unique; фільтр HTMX `?category=` |
| title | varchar(255) | | |
| sort_order | int | | |
| is_active | bool | | |
| created_at / updated_at | | | |

Seed: `keysy` (кейси), `novyny` (новини).

---

### 3.7. `blog_post`

| Колонка | Тип | Null | Примітка |
|---|---|---|---|
| id | PK | | |
| category_id | FK → blog_category | ✓ | SET_NULL |
| slug | varchar(160) | | unique → `/blog/{slug}/` |
| title | varchar(255) | | |
| excerpt | varchar(500) | ✓ | картка лістингу |
| body | text | | |
| cover_image | varchar(512) | ✓ | |
| cover_alt | varchar(255) | ✓ | |
| is_published | bool | | |
| published_at | timestamptz | ✓ | хронологія лістингу |
| seo_* | mixin | ✓ | |
| created_at / updated_at | | | |

Індекси: `(is_published, published_at DESC)`, `(category_id, published_at DESC)`.  
Share-кнопки: absolute URL з `slug` (без окремої колонки).

---

### 3.8. `leads_lead`

| Колонка | Тип | Null | Примітка |
|---|---|---|---|
| id | PK | | |
| name | varchar(120) | | ТЗ §4.1 |
| phone | varchar(30) | | |
| email | varchar(254) | | |
| consent | bool | | GDPR; має бути true при create |
| source | varchar(32) | | `home` \| `service` \| `contacts` \| `hero` |
| source_url | varchar(512) | ✓ | path сторінки відправки |
| service_id | FK → services_service | ✓ | SET_NULL; prefill з `/posluhy/{slug}/` |
| status | varchar(20) | | default `new` (ТЗ §5.3 / CRM) |
| is_read | bool | | default false (адмінка) |
| crm_external_id | varchar(64) | ✓ | **hook M5** після webhook |
| crm_synced_at | timestamptz | ✓ | |
| created_at / updated_at | | | |

**Немає** `message` / `comment` (рішення 3A).  
Check: `consent = true` на insert (валідація форми + DB check опційно).  
Індекси: `(status, created_at DESC)`, `(is_read)`, `(service_id)`.

**`status` enum (код):** `new` · `in_progress` · `closed` · `spam`

---

### 3.9. `seo_redirect_301` (M3, опційно)

| Колонка | Тип | Null | Примітка |
|---|---|---|---|
| id | PK | | |
| old_path | varchar(255) | | unique |
| new_path | varchar(255) | | |
| is_active | bool | | |
| created_at / updated_at | | | |

`/sitemap.xml` і `/robots.txt` — **без таблиць** (генерація з опублікованих моделей + `pages_site_settings.robots_extra`).

---

## 4. Що свідомо НЕ створюємо

| Кандидат | Чому ні |
|---|---|
| `team_member` / `certificate` / `metric` | Рішення 2A — у `Page.body` |
| Окремі `home_advantage` / `home_audience_item` | Рішення 1A — JSONB у `pages_home_block` |
| `lead.message` | Рішення 3A — строго ТЗ |
| `seo_keywords` / polymorphic SEO GFK | Немає в ТЗ; SeoFieldsMixin на сутностях |
| Cart / Order / Payment / User profile | Не корпоративний e-commerce |
| Quiz / multi-step lead | CTA = проста форма |
| Hero cases widget tables | Заборонено рішенням |

---

## 5. Roadmap таблиць

| Фаза | Таблиці | Статус |
|---|---|---|
| M0 Вітрина | site_settings, page, home_hero, home_block, service, category, post | Обовʼязково |
| M1 Ліди | lead (+ crm_external_id пустий) | Обовʼязково |
| M2 Адмінка | CRUD усіх вище (без нових таблиць) | Обовʼязково |
| M3 SEO | redirect_301 опційно; sitemap/robots код | Обовʼязково |
| M4 Ads/GA | без таблиць (env + GTM) | Обовʼязково |
| M5 CRM | заповнення `crm_external_id` / `crm_synced_at` | Умовно §4.4 |

---

## 6. Verify-матриця (ТЗ / карта ↔ таблиці)

| Вимога | Джерело | Таблиця / поле | Статус |
|---|---|---|---|
| Головна: hero УТП 21:9 | карта §2.2 · apps_structure | `pages_home_hero` | ✅ |
| Головна: послуги / переваги / блог teaser | ТЗ §3 · доповнення | `pages_home_block` + services/blog | ✅ |
| `/pro-nas/` текст, команда, сертифікати, метрики | ТЗ §3 | `pages_page` body | ✅ |
| `/posluhy/` + `/posluhy/{slug}/` | ТЗ §3 · карта | `services_service` | ✅ |
| `/blog/` + slug, фільтр категорій HTMX | ТЗ §3 · карта | `blog_category`, `blog_post` | ✅ |
| `/kontakty/` карта, контакти | ТЗ §3 | `pages_page` + `pages_site_settings` | ✅ |
| Політика конфіденційності | ТЗ §4.1 · карта | `pages_page` slug | ✅ |
| Форма: name, phone, email, GDPR | ТЗ §4.1 | `leads_lead` | ✅ |
| Ліди в CMS, статус Новий | ТЗ §5.3 | `leads_lead.status=new` | ✅ |
| Prefill послуги з кнопки замовлення | ТЗ §3 | `leads_lead.service_id` | ✅ |
| Meta Title/Description/H1 | ТЗ §2.5, §5.2 | SeoFieldsMixin на page/service/post | ✅ |
| sitemap.xml / robots.txt | ТЗ §2.5 | код `seo` (+ settings.robots_extra) | ✅ |
| CRM «Новий лід» | ТЗ §4.3 | `crm_external_id` hook | ✅ |
| GA4/GTM/Ads | ТЗ §4.2, §7 | поза БД | ✅ |
| Віджет кейсів у hero | рішення | — | ❌ навмисно |
| Квіз у hero | рішення | — | ❌ навмисно |

Будь-який рядок карти без покриття після реалізації моделей = блокер (ERR-BIZ-01 / ERR-SCHEMA).

---

## 7. Наступний крок

- [ ] `django_models_from_schema_skill` → `models.py` по apps  
- [ ] `seed_demo`: SiteSettings, HomeHero, 6 Services, 2 Categories, 3 Pages, sample Posts, HomeBlocks  
- [ ] Sitemap-coverage після views (карта §8)

**Документ:** `tables.md` · v1.0 · 2026-07-28
