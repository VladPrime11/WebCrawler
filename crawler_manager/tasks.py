import time
from celery import shared_task, group
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from html_parser.views import seo_analyze
from url_queue.views import get_next_url, mark_url_as_crawled


@shared_task
def run_crawler_task(url):
    start_time = time.time()

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

    result = asyncio.run(main(url))

    end_time = time.time()
    duration = end_time - start_time

    return {'result': result, 'time': duration}


@shared_task
def extract_links(html_content):
    start_time = time.time()

    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        print(f'Extracted {len(links)} links')
        result = links
    except Exception as e:
        print(f"Error extracting links: {e}")
        result = []

    end_time = time.time()
    duration = end_time - start_time

    return {'result': result, 'time': duration}


@shared_task
def deduplicate(url_list):
    start_time = time.time()

    unique_urls = list(set(url_list))
    print(f'Deduplicated list, {len(unique_urls)} unique URLs')

    end_time = time.time()
    duration = end_time - start_time

    return {'result': unique_urls, 'time': duration}


@shared_task
def add_to_queue(urls):
    start_time = time.time()

    tasks = [run_crawler_task.s(url) for url in urls]
    group(*tasks).apply_async()
    print(f'Added {len(urls)} URLs to queue')

    end_time = time.time()
    duration = end_time - start_time

    return {'result': True, 'time': duration}


@shared_task
def crawl_next_url_task():
    start_time = time.time()

    url_entry = get_next_url()

    if url_entry:
        print(f"Processing URL: {url_entry.url}")
        seo_analyze(url_entry.url)
        mark_url_as_crawled(url_entry.url)
        result = "URL processed"
    else:
        print("All URLs are processed or the queue is empty.")
        result = "No URLs to process"

    end_time = time.time()
    duration = end_time - start_time

    return {'result': result, 'time': duration}
