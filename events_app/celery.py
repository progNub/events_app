import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events_app.settings')
app = Celery('events')

# namespace = 'CELERY' для того что бы в переменных в файле settings.py отбрасывалась часть с CELERY
# то есть CELERY_ЧТО-Что-то
app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()  # это для того что бы CELERY сам нашел задачи в файлах(приложениях).
