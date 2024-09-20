from celery import shared_task, group
import asyncio
import aiohttp
from bs4 import BeautifulSoup

from html_parser.views import seo_analyze
from url_queue.views import get_next_url, mark_url_as_crawled


@shared_task
def simple_task():
    print("Задача выполняется")
    return "Задача завершена"


# Задача для выполнения парсинга страницы по URL
@shared_task
def run_crawler_task(url):
    async def fetch(session, url):
        async with session.get(url) as response:
            return await response.text()

    async def main(url):
        async with aiohttp.ClientSession() as session:
            html_content = await fetch(session, url)
            soup = BeautifulSoup(html_content, 'html.parser')
            title = soup.title.string if soup.title else 'No title'
            print(f'Parsed title: {title}')
            return title

    return asyncio.run(main(url))


# Задача для извлечения всех ссылок с страницы
@shared_task
def extract_links(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        print(f'Extracted {len(links)} links')
        return links
    except Exception as e:
        print(f"Error extracting links: {e}")
        return []


# Задача для удаления дубликатов из списка URL
@shared_task
def deduplicate(url_list):
    unique_urls = list(set(url_list))  # Простая дедупликация с помощью set
    print(f'Deduplicated list, {len(unique_urls)} unique URLs')
    return unique_urls


# Задача для добавления URL в очередь на дальнейший парсинг
@shared_task
def add_to_queue(urls):
    tasks = [run_crawler_task.s(url) for url in urls]  # Создаём задачу для каждой ссылки
    group(*tasks).apply_async()  # Запускаем задачи параллельно в группе
    print(f'Added {len(urls)} URLs to queue')
    return True


@shared_task
def crawl_next_url_task():
    """
    Celery задача для обработки следующего URL из очереди.
    """
    url_entry = get_next_url()

    if url_entry:
        print(f"Обрабатываем URL: {url_entry.url}")
        seo_analyze(url_entry.url)
        mark_url_as_crawled(url_entry.url)
    else:
        print("Все URL обработаны или очередь пуста.")
    return "Задача завершена"