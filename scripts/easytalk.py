from dotenv import load_dotenv

import fire

from hackyeah.structured_llms import structured_llm, utility_check_llm
from hackyeah.utils.url_filter import get_promising_urls, is_useful

load_dotenv()


def main(url: str = "https://www.krakow.pl/", question: str = "Gdzie znajdę informacje o studiach w Krakowie?"):
    checked = [url]
    scraped_urls = get_promising_urls(url, question, structured_llm)
    depths = {url: 1 for url in scraped_urls}

    while scraped_urls:
        new_url = scraped_urls.pop(0)
        print(f"Currently checked URL: {new_url}, depth: {depths[new_url]}")
        if is_useful(new_url, utility_check_llm, question):
            print(f"Useful url: {new_url}")
            break

        if new_url not in checked and depths[new_url] <= 3:
            promising_urls = get_promising_urls(new_url, question=question, llm=structured_llm)
            promising_urls = [promising_url for promising_url in promising_urls if promising_url not in checked]
            for url in promising_urls:
                depths[url] = depths[new_url] + 1
            scraped_urls.extend(promising_urls)
            checked.append(new_url)


if __name__ == "__main__":
    fire.Fire(main)
