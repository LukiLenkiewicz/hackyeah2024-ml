from hackyeah.scraping import get_soup, get_href_content
from hackyeah.utils.templates import TEMPLATE, UTILITY_TEMPLATE


def get_promising_urls(url, question, llm):
    soup = get_soup(url)
    elements = soup.find_all('a', href=True)
    subsites = get_href_content(url, elements)
    scraped_urls = sort_urls(question, subsites, llm)
    return scraped_urls


def sort_urls(question, subsites, llm):
    formatted_prompt = TEMPLATE.format(question=question, content=subsites)
    response = llm.invoke(formatted_prompt)
    response = response.urls
    scraped_urls = [url for url in response[:4]]
    return scraped_urls


def is_useful(website_text, llm, question):
    prompt = UTILITY_TEMPLATE.format(question=question, context=website_text)
    response = llm.invoke(prompt)
    return response.useful