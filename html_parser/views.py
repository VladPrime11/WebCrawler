import requests
from bs4 import BeautifulSoup


def fetch_html(url):
    """
    Загружает HTML-контент с веб-страницы.
    """
    try:
        response = requests.get(url)
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
    Проводит SEO-анализ страницы по URL. Извлекает заголовки, мета-теги, ссылки и текст.
    """
    html_content = fetch_html(url)

    if html_content:
        headings = extract_headings(html_content)
        print(f"Заголовки: {headings}")

        meta_tags = extract_meta_tags(html_content)
        print(f"Мета-теги: {meta_tags}")

        links = extract_links(html_content)
        print(f"Ссылки на странице: {links}")

        text = extract_text(html_content)
        print(f"Основной текст: {text[:300]}...")
    else:
        print(f"Не удалось загрузить страницу по адресу {url}")
