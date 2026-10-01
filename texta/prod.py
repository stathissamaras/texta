"""Ρυθμίσεις παραγωγής - Hetzner."""

from .settings import *   # noqa: F401,F403

DEBUG = False

ALLOWED_HOSTS = ['cartextile.gr', 'www.cartextile.gr']

CSRF_TRUSTED_ORIGINS = ['https://cartextile.gr', 'https://www.cartextile.gr']

# Το nginx τερματίζει το SSL - χωρίς αυτό το Django νομίζει ότι είναι http
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True