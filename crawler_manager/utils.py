from url_queue.models import UrlQueue


def url_queue_is_empty():
    return not UrlQueue.objects.filter(crawled=False).exists()