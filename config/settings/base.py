"""Діденко — спільні settings."""

from pathlib import Path
from urllib.parse import urlparse

from decouple import Csv, config
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())


def _database_from_url(url: str) -> dict:
    parsed = urlparse(url)
    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parsed.path.lstrip('/') or 'didenko',
        'USER': parsed.username or '',
        'PASSWORD': parsed.password or '',
        'HOST': parsed.hostname or 'localhost',
        'PORT': str(parsed.port or 5432),
        'CONN_MAX_AGE': 60,
    }


DATABASE_URL = config('DATABASE_URL', default='')
if not DATABASE_URL:
    raise RuntimeError('DATABASE_URL is required (PostgreSQL)')

DATABASES = {'default': _database_from_url(DATABASE_URL)}

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'tinymce',
    'django_htmx',
    'src.core',
    'src.pages',
    'src.services',
    'src.blog',
    'src.leads',
    'src.seo',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'src.core.context_processors.site_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'uk'
TIME_ZONE = 'Europe/Kyiv'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'default-src': ("'self'",),
        'script-src': ("'self'",),
        'style-src': (
            "'self'",
            'https://cdn.jsdelivr.net',
            'https://fonts.googleapis.com',
            # HTMX indicator <style> inject (static/js/htmx.min.js)
            "'sha256-bsV5JivYxvGywDAZ22EZJKBFip65Ng9xoJVLbBg7bdo='",
        ),
        'style-src-attr': ("'unsafe-inline'",),
        'img-src': ("'self'", 'data:', 'blob:', 'https:'),
        'font-src': ("'self'", 'https://cdn.jsdelivr.net', 'https://fonts.gstatic.com'),
        'connect-src': ("'self'",),
        'frame-src': ("'self'", 'https://www.google.com', 'https://maps.google.com'),
        'frame-ancestors': ("'none'",),
        'base-uri': ("'self'",),
        'form-action': ("'self'",),
    },
    'EXCLUDE_URL_PREFIXES': ('/admin/',),
}

TINYMCE_DEFAULT_CONFIG = {
    'height': 400,
    'menubar': False,
    'plugins': 'link lists',
    'toolbar': (
        'undo redo | fontsize | bold italic underline | '
        'bullist numlist | link | removeformat'
    ),
    'font_size_formats': '12px 14px 16px 18px 20px 24px 28px 32px',
    'content_css': False,
    'skin': 'oxide',
    'branding': False,
    'promotion': False,
}

ADMIN_NOTIFY_EMAIL = config('ADMIN_NOTIFY_EMAIL', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@example.com')
RESEND_API_KEY = config('RESEND_API_KEY', default='')
RESEND_API_URL = config(
    'RESEND_API_URL',
    default='https://api.resend.com/emails',
)
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN', default='')
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID', default='')
CRM_WEBHOOK_URL = config('CRM_WEBHOOK_URL', default='')
CRM_API_KEY = config('CRM_API_KEY', default='')
GTM_CONTAINER_ID = config('GTM_CONTAINER_ID', default='')
GA4_MEASUREMENT_ID = config('GA4_MEASUREMENT_ID', default='')

SITE_BLOCKS_CACHE_KEY = 'didenko_site_blocks_v1'
SITE_BLOCKS_CACHE_TIMEOUT = 60


def _unfold_navigation():
    from src.pages.site_content_registry import (
        build_content_sidebar_items,
        build_ui_sidebar_items,
    )

    return [
        {
            'title': 'Налаштування',
            'separator': True,
            'items': [
                {
                    'title': 'Дашборд',
                    'icon': 'dashboard',
                    'link': reverse_lazy('admin:index'),
                },
                {
                    'title': 'Налаштування сайту',
                    'icon': 'settings',
                    'link': reverse_lazy('admin:pages_sitesettings_changelist'),
                },
                {
                    'title': 'Тема сайту',
                    'icon': 'palette',
                    'link': reverse_lazy('admin:pages_activetheme_changelist'),
                },
            ],
        },
        {
            'title': 'Контент сторінок',
            'separator': True,
            'items': build_content_sidebar_items(),
        },
        {
            'title': 'Інтерфейс',
            'separator': True,
            'items': build_ui_sidebar_items(),
        },
        {
            'title': 'Списки / каталог',
            'separator': True,
            'items': [
                {
                    'title': 'Блоки головної (списки)',
                    'icon': 'view_agenda',
                    'link': reverse_lazy('admin:pages_homeblock_changelist'),
                },
                {
                    'title': 'Послуги',
                    'icon': 'gavel',
                    'link': reverse_lazy('admin:services_service_changelist'),
                },
                {
                    'title': 'Кроки процесу',
                    'icon': 'timeline',
                    'link': reverse_lazy('admin:services_processstep_changelist'),
                },
                {
                    'title': 'Інфо-сторінки',
                    'icon': 'article',
                    'link': reverse_lazy('admin:pages_page_changelist'),
                },
                {
                    'title': 'Категорії блогу',
                    'icon': 'category',
                    'link': reverse_lazy('admin:blog_category_changelist'),
                },
                {
                    'title': 'Блог / кейси',
                    'icon': 'newspaper',
                    'link': reverse_lazy('admin:blog_post_changelist'),
                },
            ],
        },
        {
            'title': 'Ліди',
            'separator': True,
            'items': [
                {
                    'title': 'Заявки',
                    'icon': 'inbox',
                    'link': reverse_lazy('admin:leads_lead_changelist'),
                },
            ],
        },
        {
            'title': 'SEO',
            'separator': True,
            'items': [
                {
                    'title': '301 редіректи',
                    'icon': 'alt_route',
                    'link': reverse_lazy('admin:seo_redirect301_changelist'),
                },
            ],
        },
    ]


UNFOLD = {
    'SITE_TITLE': 'Діденко Admin',
    'SITE_HEADER': 'Діденко — Адмінпанель',
    'SITE_SYMBOL': 'balance',
    'SITE_FAVICONS': 'src.pages.favicon.unfold_site_favicons',
    'SHOW_HISTORY': True,
    'COLORS': {
        'primary': {
            '50': '#eef2f7',
            '100': '#d9e2ef',
            '200': '#b3c5df',
            '300': '#8ca8cf',
            '400': '#6688bf',
            '500': '#2c5282',
            '600': '#1f3a5f',
            '700': '#19304f',
            '800': '#13263f',
            '900': '#0d1c2f',
            '950': '#08121f',
        },
    },
    'SIDEBAR': {
        'show_search': True,
        'show_all_applications': False,
        'navigation': _unfold_navigation(),
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {'handlers': ['console'], 'level': 'WARNING'},
    'loggers': {
        'src': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'django': {'handlers': ['console'], 'level': 'WARNING', 'propagate': False},
    },
}
