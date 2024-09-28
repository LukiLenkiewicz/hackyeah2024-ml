import os
from dotenv import load_dotenv

from groq import Groq

load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)


def get_urls(question: str, sub_urls):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Mam listę krotek zawierających informacje o podstronach pewnej strony internetowej w formacie {sub_urls} oraz pytanie od użytkownika: {question}. Posortuj te podstrony według trafności względem pytania użytkownika oraz zwróć tylko 3 najbardziej związanych podstron z pytaniem.",
            }
        ],
        model="llama-3.1-8b-instant",
    )
    return chat_completion.choices[0].message.content


sub_urls = """
[
('https://mlodziez.krakow.pl/', '+ Młodzieży', None),
 ('https://www.krakow.pl/', '', 'Bip'),
 ('https://www.krakow.pl/', 'PL', 'wersja polska'),
 ('https://www.krakow.pl/', 'Strona główna serwisu', None),
 ('https://www.krakow.pl/?dok_id=227454', 'napisz do nas', None),
 ('https://www.krakow.pl/?dok_id=242418', 'Deklaracja dostępności', None),
 ('https://www.krakow.pl/?dok_id=270941',
  'co słychać w Twojej dzielnicy',
  'co słychać w Twojej dzielnicy'),
 ('https://www.krakow.pl/biznes', 'Biznes', 'Biznes'),
 ('https://www.krakow.pl/cracovia_abierta', 'ES', 'wersja hiszpańska'),
 ('https://www.krakow.pl/cracovia_aperta', 'IT', 'wersja włoska'),
 ('https://www.krakow.pl/cracovie_ville_ouverte', 'FR', 'wersja francuska'),
 ('https://www.krakow.pl/klimat', 'Klimat', 'Klimat'),
 ('https://www.krakow.pl/komunikacja', 'Komunikacja', 'Komunikacja'),
 ('https://www.krakow.pl/krakau_weltoffene_stadt', 'DE', 'wersja niemiecka'),
 ('https://www.krakow.pl/kultura', 'Kultura', 'Kultura'),
 ('https://www.krakow.pl/lista_rss/', 'RSS', None),
 ('https://www.krakow.pl/mapa_strony/', 'Mapa strony', None),
 ('https://www.krakow.pl/nasze_miasto', 'Nasze Miasto', 'Nasze Miasto'),
 ('https://www.krakow.pl/nauka_i_edukacja',
  'Nauka i edukacja',
  'Nauka i edukacja'),
 ('https://www.krakow.pl/odwiedz_krakow', 'Odwiedź Kraków', 'Odwiedź Kraków'),
 ('https://www.krakow.pl/otofotokronika',
  'wszystkie galerie',
  'otofotokronika'),
 ('https://www.krakow.pl/samorzad/', 'Rada Miasta', 'Rada Miasta'),
 ('https://www.krakow.pl/search', 'Wyszukiwanie zaawansowane', 'zaawansowane'),
 ('https://www.krakow.pl/sport/', 'Sport i Zdrowie', 'Sport i Zdrowie')
]
"""

print(get_urls("Gdzie znajdę informacje o studiach w Krakowie?", sub_urls))
