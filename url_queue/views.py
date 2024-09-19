import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import UrlQueue


def add_url_to_queue(url):
    """
    Добавляет новый URL в очередь, если он ещё не существует.
    """
    if not UrlQueue.objects.filter(url=url).exists():
        new_url = UrlQueue(url=url)
        new_url.save()
        return True
    return False


def get_next_url():
    """
    Возвращает следующий URL для обработки, который ещё не был обработан.
    """
    next_url = UrlQueue.objects.filter(crawled=False).first()
    return next_url


def mark_url_as_crawled(url):
    """
    Помечает URL как обработанный.
    """
    try:
        url_entry = UrlQueue.objects.get(url=url)
        url_entry.crawled = True
        url_entry.save()
        return True
    except UrlQueue.DoesNotExist:
        return False

@csrf_exempt
def add_url_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            url = data.get('url')
            if url:
                added = add_url_to_queue(url)
                return JsonResponse({'success': added})
            else:
                return JsonResponse({'success': False, 'message': 'URL не найден в запросе'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Неверный формат JSON'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})