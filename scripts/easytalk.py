from dotenv import load_dotenv

import fire

from hackyeah.structured_llms import structured_llm, utility_check_llm
from hackyeah.scraping import get_soup, get_href_content
from hackyeah.utils.templates import TEMPLATE, UTILITY_TEMPLATE


load_dotenv()


def main(url: str = "https://www.krakow.pl/", question: str = "Gdzie znajdę informacje o studiach w Krakowie?"):
    checked = [url]
    scraped_urls = get_promising_urls(url, question, structured_llm)

    while scraped_urls:
        new_url = scraped_urls.pop(0)
        print(f"Currently checked URL: {new_url}")
        if is_useful(new_url, utility_check_llm, question):
            print(f"Useful url: {new_url}")
            break

        if new_url not in checked:
            promising_urls = get_promising_urls(new_url, question=question, llm=structured_llm)
            scraped_urls.extend(promising_urls)
            checked.append(new_url)


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
    scraped_urls = [url for url in response[:3]]
    return scraped_urls


def is_useful(website_text, llm, question):
    prompt = UTILITY_TEMPLATE.format(question=question, context=website_text)
    response = llm.invoke(prompt)
    return response.useful


if __name__ == "__main__":
    fire.Fire(main)
