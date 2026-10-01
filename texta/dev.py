"""Ρυθμίσεις ανάπτυξης. Τρέχει με: python manage.py runserver --settings=texta.dev"""

from .settings import *   # noqa: F401,F403

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']