# Діденко — бізнес-логіка

**Версія:** 1.0 · **Дата:** 2026-07-28  
**Джерела:** `DidenkoSitemap.pdf` · `tables.md` v1.0 · `apps_structure.md` · ТЗ Діденко  
**Регламент:** Prometey `ecommerce_business_logic_skill` (мапа URL→controller · selectors/services · coverage) + `cooperative_design`  
**Шар:** `selectors.py` (read) · `services.py` (write) · `views.py` (thin) · `urls.py`

---

## 0. Lock (рішення)

| # | Тема | Рішення |
|---|---|---|
| 1 | Фільтр блогу | `GET /blog/?category={slug}` + HTMX partial + `HX-Push-Url` |
| 2 | Пагінація блогу | **9** на сторінку (`?page=`) |
| 3 | Notify ліда | синхронно після `save`; збій notify **не** відкатує Lead |
| 4 | `is_published=False` | публічний **404** (без staff-preview у MVP) |

Правила шару:

- Views не містять ORM-фільтрів «в лоб» — лише parse → selector/service → response.
- Singleton (`SiteSettings`, `HomeHero`) — через `.load()` / `get_or_create(pk=1)`, ніколи `.first()`.
- Публічні queryset — лише `is_published=True` (+ `published_at <= now` для постів).
- Секрети інтеграцій — `.env`; у сервісах читати `settings`/decouple.

---

## 1. Мапа URL / вимога → controller

| URL / вимога | App.View | Selector / Service | Дія |
|---|---|---|---|
| `/` | `pages.HomeView` | `get_home_context()` | hero + visible blocks + teasers |
| `/pro-nas/` | `pages.PageDetailView` | `get_published_page("pro-nas")` | 404 якщо ні |
| `/kontakty/` | `pages.ContactsView` | `get_published_page("kontakty")` + `SiteSettings.load()` | body + карта/tel/email + форма |
| `/polityka-konfidentsiynosti/` | `pages.PageDetailView` | `get_published_page("polityka-konfidentsiynosti")` | |
| `/posluhy/` | `services.ServiceListView` | `list_published_services()` | sort_order ASC |
| `/posluhy/{slug}/` | `services.ServiceDetailView` | `get_published_service(slug)` | + CTA prefill service_id |
| `/blog/` | `blog.PostListView` | `list_posts(category, page)` | HTMX full або partial |
| `/blog/?category=` | той самий | фільтр + push URL | |
| `/blog/?page=` | той самий | пагінація 9 | |
| `/blog/partial/` | `blog.PostListPartialView` | той самий selector | лише сітка (HX-Request) |
| `/blog/{slug}/` | `blog.PostDetailView` | `get_published_post(slug)` | share absolute URL |
| `POST /leads/submit/` | `leads.LeadSubmitView` | `submit_lead(...)` | AJAX/HTMX; success partial |
| `/sitemap.xml` | `seo.SitemapView` | `iter_public_urls()` | |
| `/robots.txt` | `seo.RobotsView` | settings + `robots_extra` | |
| 404 / 500 | Django handlers | templates | |
| ТЗ §4.3 CRM | `leads.services.sync_lead_to_crm` | виклик з `submit_lead` якщо ключі є | |
| ТЗ §4.1 email/TG | `leads.services.notify_lead` | після save, try/except | |
| Header/footer | `core.context_processors.site` | `SiteSettings.load()` | глобально |

---

## 2. Потік даних по доменах

### 2.1. `pages` — головна

```
HomeView
  → pages.selectors.get_home_context()
       ├─ HomeHero.load()           # is_active; інакше hero=None → шаблон без секції
       ├─ list_visible_home_blocks() # is_visible, sort_order
       └─ для кожного block_type resolve_payload():
            services_teaser → services.selectors.list_published_services(limit)
            blog_teaser     → blog.selectors.list_posts(limit, category_slug?)
            advantages|audience|lead_form → лише payload JSONB (без ORM)
  → resolve_seo(page_key="home")   # з HomeHero.headline або Page/seo fallback
  → render pages/home.html
```

**Правила `resolve_home_block`:**

| block_type | Читання | Фільтр / обробка |
|---|---|---|
| `services_teaser` | `Service` | `is_published`, `sort_order`, `[:limit]` з payload (default 6) |
| `blog_teaser` | `Post` | published + optional `category_slug` + `[:limit]` (default 3) |
| `advantages` | JSONB `items[]` | як є; порожній items → секцію не рендерити |
| `audience` | JSONB | те саме |
| `lead_form` | — | у контекст лише heading/anchor; форма = partial `leads` |

CTA hero (`cta_target`): `#lead-form` → якір на секцію; `modal:lead` → JS/модалка з тим самим partial форми. Дані форми **не** з hero-моделі.

### 2.2. `pages` — інфо-сторінки

```
get_published_page(slug)
  → Page.objects.filter(slug=slug, is_published=True).first()
  → None → Http404
```

`ContactsView` додатково:

- `settings = SiteSettings.load()`
- карта: `map_embed_url` **або** lat/lng → шаблон обирає варіант
- `tel:` / `mailto:` з settings (клікабельні, ТЗ §3)
- у контекст кладе порожню `LeadForm(source="contacts")`

### 2.3. `services`

```
list_published_services(limit=None)
  qs = Service.objects.filter(is_published=True).order_by("sort_order", "id")
  return qs[:limit] if limit else qs

get_published_service(slug)
  → get_object_or_404(Service, slug=slug, is_published=True)
```

На деталі:

- SEO: `seo_title|title`, `seo_description|short_description`, `seo_h1|title`
- Форма: `LeadForm(initial={"service_id": service.pk}, source="service")`
- Кнопка «Замовити» → той самий submit endpoint

Немає faceted-фільтрів послуг у MVP (каталог плоский).

### 2.4. `blog` — список, фільтр, пагінація

**Вхід query:**

| Параметр | Обробка |
|---|---|
| `category` | slug активної категорії; невідомий slug → ігнор (як без фільтра) **або** порожній список? → **ігнор + усі пости** (мʼякше для UX) |
| `page` | int ≥ 1; default 1; out-of-range → остання / порожня сторінка Django Paginator |

```
list_posts(*, category_slug=None, page=1, per_page=9, limit=None)
  qs = Post.objects.filter(
         is_published=True,
         published_at__lte=timezone.now(),
       ).select_related("category").order_by("-published_at", "-id")
  if category_slug:
      cat = Category.objects.filter(slug=category_slug, is_active=True).first()
      if cat:
          qs = qs.filter(category=cat)
  if limit is not None:          # teaser на головній
      return qs[:limit]
  return Paginator(qs, per_page).get_page(page)
```

**HTMX (рішення 1A):**

1. Повний захід `/blog/` → `PostListView` (сторінка + фільтри + сітка).
2. Клік категорії / пагінація з `hx-get="/blog/partial/?category=&page="` + `hx-target="#blog-grid"` + `hx-push-url="/blog/?category=&page="`.
3. `PostListPartialView`: якщо немає `HX-Request` → redirect на канонічний `/blog/?…`.
4. Канонічний URL у `<link rel="canonical">` — **без** query для SEO base **або** з category якщо фільтр = окремий інтент; MVP: canonical = `/blog/` (фільтр — UX), щоб не плодити індексацію. Пагінація `page>1` — `noindex` або `rel=prev/next` (seo_skill); мінімум: canonical на `/blog/`.

`list_active_categories()` — для чіпсів фільтра: `is_active=True`, `sort_order`.

### 2.5. `blog` — деталь

```
get_published_post(slug)
  → filter(is_published=True, published_at__lte=now, slug=slug)
  → 404 якщо немає

absolute_share_url(request, post) → request.build_absolute_uri(post.get_absolute_url())
```

Кнопки «Поділитися» у шаблоні з цим URL (ТЗ §3).

### 2.6. `leads` — подача заявки

```
POST /leads/submit/   (HTMX або fetch)
  → honeypot порожній
  → LeadForm.is_valid()
       обовʼязкові: name, phone, email, consent=True
       service_id: optional; якщо передано — має існувати published Service
  → leads.services.submit_lead(cleaned, *, source, source_url, request)
```

**`submit_lead` (atomic лише на create):**

```
1. transaction.atomic:
     Lead.objects.create(
       name, phone, email, consent=True,
       source, source_url,
       service_id, status="new", is_read=False,
     )
2. try: notify_lead(lead)          # email адміна + Telegram якщо токени
   except: log.exception; НЕ raise
3. try: sync_lead_to_crm(lead)     # якщо CRM_URL/KEY; пише crm_external_id / crm_synced_at
   except: log.exception; НЕ raise
4. return lead
```

**Відповіді view:**

| Стан | HTMX | JSON/звичайний |
|---|---|---|
| OK | `200` + `partials/lead_success.html` («Дякуємо за заявку») | 200 JSON `{ok: true}` |
| Invalid | `422` + form partial з помилками | 422 + errors |
| Honeypot | `200` success fake (антибот) | 200 ok |

`source` визначає view з hidden field або referer map: `home` | `hero` | `service` | `contacts`.

Валідація телефону/email — на формі (ТЗ §6 кейс 2); service повторно не дублює UI-повідомлення, лише integrity.

### 2.7. `seo`

```
iter_public_urls():
  yield "/" 
  yield published pages (get_absolute_url)
  yield /posluhy/ + кожен published service
  yield /blog/ + кожен published post
  (+ lastmod = updated_at / published_at)

robots.txt:
  User-agent: *
  Disallow: /admin/
  Disallow: /leads/
  Sitemap: {ABS}/sitemap.xml
  + SiteSettings.robots_extra
```

Опційно M3: middleware/view `seo_redirect_301` — exact `old_path` → 301 `new_path` якщо `is_active`.

### 2.8. SEO resolve (усі публічні сторінки)

```
resolve_seo(entity | None, *, defaults):
  title = entity.seo_title or defaults["title"]
  description = entity.seo_description or defaults["description"]
  h1 = entity.seo_h1 or defaults["h1"]
```

OG: title/description + absolute image (hero/cover) якщо є.

---

## 3. Шари по apps (контракт функцій)

### `pages.selectors`

| Функція | Поведінка |
|---|---|
| `SiteSettings.load()` | get_or_create(pk=1) |
| `HomeHero.load()` | get_or_create(pk=1); якщо не is_active → None для вітрини |
| `list_visible_home_blocks()` | is_visible, order by sort_order |
| `get_home_context()` | збирає hero, blocks, resolved teasers |
| `get_published_page(slug)` | або None |

### `pages.services`

| Функція | Поведінка |
|---|---|
| — (MVP) | записи лише через admin; публічних write немає |

### `services.selectors`

| Функція | Поведінка |
|---|---|
| `list_published_services(limit=None)` | published, sort_order |
| `get_published_service(slug)` | або 404 helper |

### `blog.selectors`

| Функція | Поведінка |
|---|---|
| `list_active_categories()` | is_active, sort_order |
| `list_posts(...)` | див. §2.4 |
| `get_published_post(slug)` | published + published_at |

### `leads.services`

| Функція | Поведінка |
|---|---|
| `submit_lead(...)` | create + notify + crm (§2.6) |
| `notify_lead(lead)` | email + Telegram; swallow errors |
| `sync_lead_to_crm(lead)` | webhook; update external_id; swallow errors |
| `mark_lead_read(lead, user)` | admin-only; perm check у service якщо кастом-екшен |

### `seo.selectors`

| Функція | Поведінка |
|---|---|
| `iter_public_urls()` | §2.7 |
| `get_active_redirect(path)` | M3 |

---

## 4. Порядок реалізації (dependency chain)

```
1. core mixins + context_processor SiteSettings
2. pages (settings, page, hero, blocks) + HomeView + PageDetail
3. services list/detail
4. blog list/partial/detail (filter + paginate)
5. leads form + submit_lead + notify stubs
6. seo sitemap/robots
7. ContactsView (page + settings + form)
8. seed_demo + sitemap-coverage verify
9. CRM sync (M5, коли є ключі)
```

---

## 5. Sitemap-coverage verify

| URL з карти | urls | View | Selector/Service | Шаблон | Навігація | Статус |
|---|---|---|---|---|---|---|
| `/` | ☐ | ☐ | `get_home_context` | ☐ | ☐ | план ✅ |
| `/pro-nas/` | ☐ | ☐ | `get_published_page` | ☐ | ☐ | план ✅ |
| `/posluhy/` | ☐ | ☐ | `list_published_services` | ☐ | ☐ | план ✅ |
| `/posluhy/{slug}/` | ☐ | ☐ | `get_published_service` | ☐ | ☐ | план ✅ |
| `/blog/` | ☐ | ☐ | `list_posts` | ☐ | ☐ | план ✅ |
| `/blog/{slug}/` | ☐ | ☐ | `get_published_post` | ☐ | ☐ | план ✅ |
| `/kontakty/` | ☐ | ☐ | page + settings | ☐ | ☐ | план ✅ |
| `/polityka-konfidentsiynosti/` | ☐ | ☐ | `get_published_page` | ☐ | ☐ | план ✅ |
| `/sitemap.xml` | ☐ | ☐ | `iter_public_urls` | — | — | план ✅ |
| `/robots.txt` | ☐ | ☐ | robots builder | — | — | план ✅ |
| `POST /leads/submit/` | ☐ | ☐ | `submit_lead` | partial | — | план ✅ (службовий) |

Після коду — проставити ✅/❌ по колонках; рядок без статусу = блокер (ERR-BIZ-01).

---

## 6. Security / якість (мінімум)

| ID | Правило |
|---|---|
| L-01 | CSRF на POST форми |
| L-02 | Honeypot + rate limit (опційно cache по IP) |
| L-03 | `consent` обовʼязковий True; без нього не create |
| L-04 | `service_id` лише published; інакше form error |
| L-05 | Не віддавати staff-only поля в публічних шаблонах |
| L-06 | HTML `Page.body` / `Post.body` — sanitize на save або safe+trusted admin only |
| L-07 | Notify/CRM exceptions не ламають UX успіху |

---

## 7. E2E ↔ логіка (ТЗ §6)

| # | Кейс | Ланцюжок |
|---|---|---|
| 1 | Заявка OK | form → `submit_lead` → Lead `new` → success partial; notify best-effort |
| 2 | Некоректні дані | form errors → 422 partial; Lead не створюється |
| 3 | Mobile | поза цим документом (UI); меню/форма ті самі endpoints |
| 4 | Навігація | усі URL з §1; unpublished → 404 |

---

**Документ:** `business_logic.md` · v1.0 · 2026-07-28  
**Наступний крок:** scaffold Django + models з `tables.md` → реалізація selectors/services за цим файлом.
