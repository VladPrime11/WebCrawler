from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from data_storage.models import ParsedContent
from url_queue.views import add_url_to_queue


def fetch_html(url):
    """
    Загружает HTML-контент с веб-страницы, добавляя заголовок User-Agent для обхода блокировок.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Не удалось загрузить страницу {url}. Статус-код: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Ошибка при загрузке страницы {url}: {e}")
        return None


def extract_headings(html_content):
    """
    Извлекает заголовки h1, h2, h3 со страницы.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    headings = {
        'h1': [h1.text.strip() for h1 in soup.find_all('h1')],
        'h2': [h2.text.strip() for h2 in soup.find_all('h2')],
        'h3': [h3.text.strip() for h3 in soup.find_all('h3')],
    }
    return headings


def extract_meta_tags(html_content):
    """
    Извлекает мета-теги title, description и keywords.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    meta_data = {
        'title': soup.title.string.strip() if soup.title else 'Нет тега title',
        'description': '',
        'keywords': ''
    }

    description_tag = soup.find('meta', attrs={'name': 'description'})
    if description_tag and description_tag.get('content'):
        meta_data['description'] = description_tag['content'].strip()

    keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
    if keywords_tag and keywords_tag.get('content'):
        meta_data['keywords'] = keywords_tag['content'].strip()

    return meta_data


def extract_links(html_content):
    """
    Извлекает все ссылки (атрибут href) на странице.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return links


def extract_text(html_content):
    """
    Извлекает основной текст страницы (теги p).
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = [p.text.strip() for p in soup.find_all('p')]
    return ' '.join(paragraphs)


def seo_analyze(url):
    """
    Проводит SEO-анализ страницы по URL, сохраняет результаты и добавляет найденные ссылки в очередь.
    """
    html_content = fetch_html(url)

    if html_content:
        headings = extract_headings(html_content)
        meta_tags = extract_meta_tags(html_content)
        links = extract_links(html_content)
        text = extract_text(html_content)

        save_parsed_content(url, headings, meta_tags, links, text)

        for link in links:
            absolute_url = urljoin(url, link)
            add_url_to_queue(absolute_url)

        print(f"Результаты для {url} сохранены и ссылки добавлены в очередь.")
    else:
        print(f"Не удалось загрузить страницу по адресу {url}")


def save_parsed_content(url, headings, meta_tags, links, text):
    """
    Сохраняет результаты парсинга страницы в базу данных с читаемыми символами.
    """
    parsed_content = ParsedContent(
        url=url,
        title=meta_tags.get('title', ''),
        description=meta_tags.get('description', ''),
        keywords=meta_tags.get('keywords', ''),
        headings=headings,
        text=text[:1000],
        links=links
    )

    parsed_content.save()


