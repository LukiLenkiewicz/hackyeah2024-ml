import os
from langchain.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(api_key=os.getenv("OPENAI_APIKEY"), temperature=0.1)


summarize_html_template = """
"Otrzymałeś kod HTML strony internetowej. Twoim zadaniem jest podsumowanie strony w sposób zwięzły i dokładny dla użytkownika końcowego. W podsumowaniu uwzględnij:

1. Tytuł strony.
2. Krótką informację, co znajduje się na stronie.
3. Jakie funkcje są dostępne na stronie (np. formularze, przyciski, opcje logowania, wyszukiwarka itp.).
4. Co użytkownik może zrobić na tej stronie.

Podaj wyłącznie istotne informacje bez zbędnego powtarzania się, skupiając się na funkcjonalności i treści ważnej dla użytkownika końcowego."

KOD HTML STRONY:
{html}
"""

summarize_html_prompt = PromptTemplate(
    input_variables=["html"], template=summarize_html_template
)

summary_html_chain = load_summarize_chain(
    chain_type="stuff",
    llm=llm,
    prompt=summarize_html_prompt,
    document_variable_name="html",
)

# example usage

# html = ""

# doc_html = Document(page_content=html)

# res = summary_html_chain.invoke([doc_html])
# print(res["output_text"])
