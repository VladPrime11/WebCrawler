from django.http import JsonResponse
from crawler_manager.tasks import crawl_next_url_task

def trigger_crawl_task(request):
    """
    Запускает задачу для обработки следующего URL.
    """
    result = crawl_next_url_task.delay()  # Запускаем задачу в Celery
    return JsonResponse({'task_id': result.task_id, 'status': 'Task started'})
