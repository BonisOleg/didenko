"""Реєстрація proxy CMS-секцій у адмінці."""

from django.contrib import admin
from unfold.admin import ModelAdmin

from src.pages.admin_utils import ContentSectionAdminMixin
from src.pages.models_proxies import (
    BlogPageSettings,
    ContactsPageSettings,
    HomeAdvantagesSettings,
    HomeAudienceSettings,
    HomeBlogSettings,
    HomeHeroSettings,
    HomeLeadSettings,
    HomeServicesSettings,
    ServicesPageSettings,
    SiteBrandSettings,
    SiteFooterSettings,
    SiteFormsSettings,
    SiteNavigationSettings,
)


class SiteContentSectionAdmin(ContentSectionAdminMixin, ModelAdmin):
    pass


_SECTION_MODELS: tuple[tuple[type, str, str], ...] = (
    (HomeHeroSettings, 'home', 'hero'),
    (HomeAudienceSettings, 'home', 'audience'),
    (HomeServicesSettings, 'home', 'services'),
    (HomeAdvantagesSettings, 'home', 'advantages'),
    (HomeBlogSettings, 'home', 'blog'),
    (HomeLeadSettings, 'home', 'lead'),
    (ServicesPageSettings, 'services', 'page'),
    (ContactsPageSettings, 'contacts', 'page'),
    (BlogPageSettings, 'blog', 'page'),
    (SiteBrandSettings, 'site', 'brand'),
    (SiteNavigationSettings, 'site', 'navigation'),
    (SiteFooterSettings, 'site', 'footer'),
    (SiteFormsSettings, 'site', 'forms'),
)


def register_site_content_section_admins() -> None:
    for model_cls, page_slug, section_slug in _SECTION_MODELS:
        admin_cls = type(
            f'{model_cls.__name__}Admin',
            (SiteContentSectionAdmin,),
            {
                'page_slug': page_slug,
                'section_slug': section_slug,
                'change_url_name': f'admin:pages_{model_cls._meta.model_name}_change',
            },
        )
        if model_cls not in admin.site._registry:
            admin.site.register(model_cls, admin_cls)
