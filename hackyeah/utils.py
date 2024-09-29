import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

cookies = dict(language='pl_PL')

# Function to get website text
def get_website_text(url):
    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')
    except (requests.RequestException, Exception) as e:
        print(f"Failed to access {url}: {e}")
        return
    
    tag = soup.body
 
    # Print each string recursively
    website_text = ''
    for string in tag.strings:
        if string.strip():
            website_text += string.strip() + '\n'
    
    return website_text

def join_description(title, text):
    desc = ''
    if title:
        desc += title
    if text and text != title:
        if desc:
            desc += ' - '
        desc += text
    
    return desc

# Function to find subsites with info
def find_subsites_with_info(url):
    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()  # Check if the request was successful
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
        
        if "#" in href or "?" in href or "mailto:" in href or "tel:" in href:
            continue
        link = urljoin(url, href)
        subsites.add((link, text, title))
        

    subsites = [{'url': subsite[0], 'description': join_description(subsite[1], subsite[2])} for subsite in subsites]
    
    return subsites