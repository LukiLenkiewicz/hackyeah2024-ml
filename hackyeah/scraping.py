import logging
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import pprint

cookies = dict(language='pl_PL')


def find_subsites_with_info(url):
    soup = get_soup(url)
    website_text = get_website_text(soup)

    elements = soup.find_all('a', href=True)

    subsites = get_href_content(url, elements)
    return list(subsites), website_text


def get_soup(url):
    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except (requests.RequestException, Exception) as e:
        print(f"Failed to access {url}: {e}")
        return

    return soup


def get_website_text(soup):
    tag = soup.body
 
    website_text = ''
    for string in tag.strings:
        if string.strip():
            website_text += string.strip() + '\n'
    return website_text        


def get_href_content(url, elements):
    subsites = set()
    for element in elements:
        href = element['href']
        text = element.text.strip()
        title = element.get('title')
        
        if href.startswith('http') or href.startswith('https') or href.endswith('html'):
            continue
        
        link = urljoin(url, href)
        subsites.add((link, text, title))
        
    subsites = [{'url': subsite[0], 'description': f"{subsite[2]} - {subsite[1]}"} for subsite in subsites]
    return subsites
