import logging
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)
logging.getLogger("bs4").setLevel(logging.ERROR)

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import pprint

cookies = dict(language='pl_PL')

def find_subsites_with_info(url):
    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except (requests.RequestException, Exception) as e:
        print(f"Failed to access {url}: {e}")
        return
    
    elements = soup.find_all('a', href=True)
    
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
    return list(subsites)

subsites = find_subsites_with_info("https://www.krakow.pl/")
pprint.pprint(subsites)