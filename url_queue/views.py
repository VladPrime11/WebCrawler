import json

from django.core.validators import URLValidator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

from .models import UrlQueue


def add_url_to_queue(url):
    if not UrlQueue.objects.filter(url=url).exists():
        new_url = UrlQueue(url=url)
        new_url.save()
        print(f"URL {url} added to the queue.")
        return True
    return False


def get_next_url():
    next_url = UrlQueue.objects.filter(crawled=False).first()
    return next_url


def mark_url_as_crawled(url):
    try:
        url_entry = UrlQueue.objects.get(url=url)
        url_entry.crawled = True
        url_entry.save()
        return True
    except UrlQueue.DoesNotExist:
        return False


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)
        return True
    except ValidationError:
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
                return JsonResponse({'success': False, 'message': 'URL not found in the request'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def clear_queue():
    UrlQueue.objects.all().delete()
    print("Queue cleared.")
    return True


@csrf_exempt
def clear_queue_view(request):
    if request.method == "POST":
        cleared = clear_queue()
        return JsonResponse({'success': cleared})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
