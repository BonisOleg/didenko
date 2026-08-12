"""Docker / Droplet settings.

TLS terminates in nginx. Gunicorn stays HTTP so /healthz/ is not 301.
"""

from .production import *  # noqa: F403

SECURE_SSL_REDIRECT = False
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

_extra_hosts = ['web', '127.0.0.1', 'localhost']
ALLOWED_HOSTS = list(  # noqa: F405
    dict.fromkeys([*ALLOWED_HOSTS, *_extra_hosts]),  # noqa: F405
)

SILENCED_SYSTEM_CHECKS = ['security.W008']
