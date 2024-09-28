import os
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(api_key=os.getenv("OPENAI_APIKEY"), temperature=0.1)

rank_url_template = """
Mam listę krotek zawierających informacje o podstronach pewnej strony internetowej w formacie {sub_urls}, gdzie każda krotka zawiera: adres URL podstrony, krótki opis oraz tytuł linku. Użytkownik zadał pytanie: '{question}'.

Zwróć tylko 3 najbardziej związane podstrony z zapytaniem, biorąc pod uwagę:
1. Zawartość opisu i tytułu linku, które powinny zawierać słowa kluczowe związane z pytaniem.
2. Tematyka podstrony, która powinna odpowiadać pytaniu użytkownika.

Proszę zwrócić jedynie adresy URL najbardziej odpowiednich podstron, bez uzasadnienia wyborów.
"""


rank_url_prompt = PromptTemplate(
    input_variables=["sub_urls", "question"], template=rank_url_template
)

rank_url_chain = rank_url_prompt | llm


def get_urls(question: str, sub_urls: str):
    res = rank_url_chain.invoke(
        {"sub_urls": sub_urls, "question": question}
    )  # Directly pass as keyword arguments
    return res


# sub_urls = """
# [
# ('https://mlodziez.krakow.pl/', '+ Młodzieży', None),
#  ('https://www.krakow.pl/', '', 'Bip'),
#  ('https://www.krakow.pl/', 'PL', 'wersja polska'),
#  ('https://www.krakow.pl/', 'Strona główna serwisu', None),
#  ('https://www.krakow.pl/?dok_id=227454', 'napisz do nas', None),
#  ('https://www.krakow.pl/?dok_id=242418', 'Deklaracja dostępności', None),
#  ('https://www.krakow.pl/?dok_id=270941', 'co słychać w Twojej dzielnicy', 'co słychać w Twojej dzielnicy'),
#  ('https://www.krakow.pl/biznes', 'Biznes', 'Biznes'),
#  ('https://www.krakow.pl/cracovia_abierta', 'ES', 'wersja hiszpańska'),
#  ('https://www.krakow.pl/cracovia_aperta', 'IT', 'wersja włoska'),
#  ('https://www.krakow.pl/cracovie_ville_ouverte', 'FR', 'wersja francuska'),
#  ('https://www.krakow.pl/klimat', 'Klimat', 'Klimat'),
#  ('https://www.krakow.pl/komunikacja', 'Komunikacja', 'Komunikacja'),
#  ('https://www.krakow.pl/krakau_weltoffene_stadt', 'DE', 'wersja niemiecka'),
#  ('https://www.krakow.pl/kultura', 'Kultura', 'Kultura'),
#  ('https://www.krakow.pl/lista_rss/', 'RSS', None),
#  ('https://www.krakow.pl/mapa_strony/', 'Mapa strony', None),
#  ('https://www.krakow.pl/nasze_miasto', 'Nasze Miasto', 'Nasze Miasto'),
#  ('https://www.krakow.pl/nauka_i_edukacja', 'Nauka i edukacja', 'Nauka i edukacja'),
#  ('https://www.krakow.pl/odwiedz_krakow', 'Odwiedź Kraków', 'Odwiedź Kraków'),
#  ('https://www.krakow.pl/otofotokronika', 'wszystkie galerie', 'otofotokronika'),
#  ('https://www.krakow.pl/samorzad/', 'Rada Miasta', 'Rada Miasta'),
#  ('https://www.krakow.pl/search', 'Wyszukiwanie zaawansowane', 'zaawansowane'),
#  ('https://www.krakow.pl/sport/', 'Sport i Zdrowie', 'Sport i Zdrowie')
# ]
# """

# example usage
# print(get_urls("Gdzie znajdę informacje o szpitalach w Krakowie?", sub_urls))
