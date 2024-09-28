import os
from dotenv import load_dotenv

import fire
from langchain_openai import OpenAI

from hackyeah.general_scraping import find_subsites_with_info
from hackyeah.templates import TEMPLATE

load_dotenv()

llm = OpenAI(temperature=0.1)


def main(url: str = "https://www.krakow.pl/", question: str = "Gdzie znajdę informacje o studiach w Krakowie?"):
    content = find_subsites_with_info(url)
    formatted_prompt = TEMPLATE.format(question=question, content=content)
    result = llm.invoke(formatted_prompt)
    print(result)


if __name__ == "__main__":
    fire.Fire(main)
