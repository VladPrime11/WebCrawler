from urllib.parse import urljoin

import requests
import random
from bs4 import BeautifulSoup
from data_storage.models import ParsedContent
from url_queue.views import add_url_to_queue


def fetch_html(url):
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1'
    ]

    headers = {
        'User-Agent': random.choice(user_agents)
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to load the page {url}. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error on page loading {url}: {e}")
        return None


def extract_headings(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    headings = {
        'h1': [h1.text.strip() for h1 in soup.find_all('h1')],
        'h2': [h2.text.strip() for h2 in soup.find_all('h2')],
        'h3': [h3.text.strip() for h3 in soup.find_all('h3')],
    }
    return headings


def extract_meta_tags(html_content):
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
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return links


def extract_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = [p.text.strip() for p in soup.find_all('p')]
    return ' '.join(paragraphs)


def seo_analyze(url):
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

        print(f"Results for {url} saved and links added to the queue.")
    else:
        print(f"Failed to load the page at {url}")


def save_parsed_content(url, headings, meta_tags, links, text):
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


