from url_queue.views import get_next_url, mark_url_as_crawled
from html_parser.views import seo_analyze


def crawl_next_url():
    """
    Извлекает следующий URL из очереди, анализирует его с помощью seo_analyze и помечает как обработанный.
    """
    url_entry = get_next_url()

    if url_entry:
        print(f"Обрабатываем URL: {url_entry.url}")
        seo_analyze(url_entry.url)

        mark_url_as_crawled(url_entry.url)
    else:
        print("Все URL обработаны или очередь пуста.")
