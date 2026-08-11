"""Proxy-моделі CMS-секцій (sidebar Unfold)."""

from src.pages.models import SiteSettings


class HomeHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Hero'
        verbose_name_plural = 'Головна — Hero'


class HomeAudienceSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Для кого'
        verbose_name_plural = 'Головна — Для кого'


class HomeServicesSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Послуги'
        verbose_name_plural = 'Головна — Послуги'


class HomeAdvantagesSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Переваги'
        verbose_name_plural = 'Головна — Переваги'


class HomeBlogSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Блог'
        verbose_name_plural = 'Головна — Блог'


class HomeLeadSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Заявка'
        verbose_name_plural = 'Головна — Заявка'


class ServicesPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Послуги — сторінка'
        verbose_name_plural = 'Послуги — сторінка'


class ContactsPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Контакти — сторінка'
        verbose_name_plural = 'Контакти — сторінка'


class BlogPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Блог — сторінка'
        verbose_name_plural = 'Блог — сторінка'


class SiteBrandSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Бренд / логотипи'
        verbose_name_plural = 'Бренд / логотипи'


class SiteNavigationSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Навігація'
        verbose_name_plural = 'Навігація'


class SiteFooterSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Footer'
        verbose_name_plural = 'Footer'


class SiteFormsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Форми / модалки'
        verbose_name_plural = 'Форми / модалки'
