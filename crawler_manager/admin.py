from django.contrib import admin
from django.http import HttpResponse
from django_celery_results.models import TaskResult  # Модель для хранения результатов задач
import subprocess
import redis

from .models import CeleryControl
from celery.result import AsyncResult

r = redis.StrictRedis(host='localhost', port=6379, db=0)


@admin.register(CeleryControl)
class CeleryControlAdmin(admin.ModelAdmin):
    change_list_template = "admin/celery_control_changelist.html"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('start-worker/', self.start_worker, name='start-worker'),
            path('stop-worker/', self.stop_worker, name='stop-worker'),
            path('start-beat/', self.start_beat, name='start-beat'),
            path('stop-beat/', self.stop_beat, name='stop-beat'),
        ]
        return custom_urls + urls

    def start_worker(self, request):
        subprocess.Popen(['celery', '-A', 'WebCrawler', 'worker', '--pool=solo', '--loglevel=info'])
        self.message_user(request, "Celery worker запущен в режиме solo.")
        return HttpResponse("Celery worker запущен в режиме solo.")

    def stop_worker(self, request):
        subprocess.Popen(['pkill', '-f', 'celery worker'])
        self.message_user(request, "Celery worker остановлен.")
        return HttpResponse("Celery worker остановлен.")

    def start_beat(self, request):
        subprocess.Popen(['celery', '-A', 'WebCrawler', 'beat', '--loglevel=info'])
        self.message_user(request, "Celery Beat запущен.")
        return HttpResponse("Celery Beat запущен.")

    def stop_beat(self, request):
        subprocess.Popen(['pkill', '-f', 'celery beat'])
        self.message_user(request, "Celery Beat остановлен.")
        return HttpResponse("Celery Beat остановлен.")

    def get_task_statistics(self):
        task_ids = r.keys('celery-task-meta-*')

        completed_tasks = 0
        total_time = 0
        for task_id in task_ids:
            result = AsyncResult(task_id.decode('utf-8').replace('celery-task-meta-', ''))
            if result.status == 'SUCCESS':
                completed_tasks += 1
                task_result = result.result

                if isinstance(task_result, dict):
                    time_spent = task_result.get('time', 0)
                    total_time += time_spent
                else:
                    pass

        avg_duration = total_time / completed_tasks if completed_tasks > 0 else 0
        return completed_tasks, avg_duration

    def changelist_view(self, request, extra_context=None):
        completed_tasks, avg_duration = self.get_task_statistics()

        extra_context = extra_context or {}
        extra_context['completed_tasks'] = completed_tasks
        extra_context['avg_duration'] = avg_duration

        return super().changelist_view(request, extra_context=extra_context)

    def task_count_display(self, obj=None):
        completed_tasks, _ = self.get_task_statistics()
        return f"Выполнено задач: {completed_tasks}"

    def avg_duration_display(self, obj=None):
        _, avg_duration = self.get_task_statistics()
        return f"Среднее время выполнения: {avg_duration:.2f} сек"

    list_display = ['task_count_display', 'avg_duration_display']
