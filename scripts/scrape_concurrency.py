import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
import re


def fetch_and_parse(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            urls = set()
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                full_url = urljoin(url, href)
                if urlparse(full_url).netloc == urlparse(url).netloc:
                    urls.add(full_url)
            return urls
        else:
            print(f"Failed to retrieve {url} - Status code: {response.status_code}")
            return set()
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return set()

def scrape(url, max_depth=3, visited=None, executor=None):
    if visited is None:
        visited = set()
    if max_depth == 0 or url in visited:
        return

    print(f"Scraping {url}")
    visited.add(url)

    urls = fetch_and_parse(url)
    
    futures = []
    for u in urls:
        if u not in visited:
            futures.append(executor.submit(scrape, u, max_depth - 1, visited, executor))

    for future in futures:
        future.result()

def main(start_url, max_depth=2):
    with ThreadPoolExecutor(max_workers=3) as executor:
        scrape(start_url, max_depth, executor=executor)

start_url = 'https://www.krakow.pl/'
max_depth = 3
main(start_url, max_depth)
