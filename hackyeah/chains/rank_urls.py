import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


# Define the structured response model using pydantic
class RankedURLs(BaseModel):
    urls: list[str]  # A list of 3 relevant URLs


# Wrap the LLM with the structured output that conforms to RankedURLs
model = ChatOpenAI(temperature=0, api_key=os.getenv("OPENAI_APIKEY"))
structured_llm = model.with_structured_output(RankedURLs)


# Define the prompt template for ranking the URLs based on the question
rank_url_template = """
Mam listę krotek zawierających informacje o podstronach pewnej strony internetowej w formacie {sub_urls}, gdzie każda krotka zawiera: adres URL podstrony, krótki opis oraz tytuł linku. Użytkownik zadał pytanie: '{question}'.

Zwróć tylko 2 najbardziej związane podstrony z zapytaniem, biorąc pod uwagę:
1. Zawartość opisu i tytułu linku, które powinny zawierać słowa kluczowe związane z pytaniem.
2. Tematyka podstrony, która powinna odpowiadać pytaniu użytkownika.

Proszę zwrócić jedynie adresy URL najbardziej odpowiednich podstron, bez uzasadnienia wyborów.
"""

# Create the prompt template for passing the sub_urls and question
rank_url_prompt = PromptTemplate(
    input_variables=["sub_urls", "question"], template=rank_url_template
)

# Combine the prompt template with the structured LLM
rank_url_chain = rank_url_prompt | structured_llm


# Function to get the ranked URLs based on the user's question
def get_urls(question: str, sub_urls: str):
    # Invoke the LLM with the given sub_urls and question
    res = rank_url_chain.invoke({"sub_urls": sub_urls, "question": question})

    # The response is already in structured format, we can directly access the urls list
    return res.urls  # This will return the list of 3 most relevant URLs
