from langchain_community.cache import SQLiteCache
from langchain.globals import set_llm_cache
from typing import Tuple

from .utils import get_website_text, find_subsites_with_info
from .llms import extract_relevant_subsites, classify_relevance, chat_with_website

# Step 1: Main pipeline function
def pipeline(url: str, question: str) -> Tuple[str, str]:
    ALREADY_CHECKED = set()
    RELEVANT_SUBSITES = [url]
    DEPTHS = {url: 0}
    
    while RELEVANT_SUBSITES:
        print(RELEVANT_SUBSITES)
        subsite = RELEVANT_SUBSITES.pop(0)
        if DEPTHS[subsite] >= 3:
            continue
        print(f"Checking subsite: {subsite}")
        
        # Step 2: Get website text
        website_text = get_website_text(subsite)

        # Step 3: Classify relevance
        relevance_response = classify_relevance(question, website_text)
        
        # Step 4: Check if response indicates relevance
        if "TRUE" in relevance_response:
            # Placeholder for further implementation
            print(f"Relevance confirmed for website {subsite}.")
            result = chat_with_website(subsite, question)
            key = list(result.keys())[0]
            print("Retrieved information:")
            print(result[key])
            return subsite, result[key]
        else:         
            ALREADY_CHECKED.add(subsite)
            # Step 5: Find subsites
            subsites_with_info = find_subsites_with_info(subsite)
            
            # Step 6: Extract relevant subsites
            relevant_subsites = extract_relevant_subsites(subsites_with_info, question)
            
            # Step 7: Append relevant subsites to the top of the list
            for new_subsite in relevant_subsites[::-1]:
                if not isinstance(new_subsite, dict):
                    continue
                if new_subsite['url'] not in RELEVANT_SUBSITES and new_subsite['url'] not in ALREADY_CHECKED:
                    RELEVANT_SUBSITES.insert(0, new_subsite['url'])
                    DEPTHS[new_subsite['url']] = DEPTHS[subsite] + 1

if __name__ == "__main__":
    set_llm_cache(SQLiteCache(database_path="./cache.db"))
    
    # Example usage
    # pipeline("https://www.wroclaw.pl/", "Sprawdź aktualne informacje sportowe.")
    # pipeline("https://www.wroclaw.pl/", "Chcę znaleźć numer kontaktowy do MPK Wrocław.")
    # pipeline("https://www.wroclaw.pl/", "Jakie są zmiany w kursach autobusów spowodowane powodzią?")
    # pipeline("https://www.krakow.pl/", "Jakie są atrakcje w Krakowie?")
    # pipeline("https://hypmar.com/", "Jakie prace realizuje firma Hypmar?")
    # pipeline("https://ai.pwr.edu.pl/", "Kto zajmuje pozycję kierownika katedry?")
    pipeline("https://hackyeah.pl/", "Do której godziny jest deadline zgłoszeń na HackYeah?")