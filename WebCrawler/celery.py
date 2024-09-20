from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Устанавливаем модуль настроек Django по умолчанию для 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebCrawler.settings')

app = Celery('WebCrawler')

# Читаем настройки Django с префиксом "CELERY_"
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи в установленных приложениях
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
