"""
WSGI config for events_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""
import os
import sys
from django.core.wsgi import get_wsgi_application

# Добавляем каталог с проектом в sys.path
sys.path.append('/home/yastreb/events')

# Указываем Django, какие настройки использовать
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "events_app.settings")

# Создаем WSGI-приложение Django
application = get_wsgi_application()

