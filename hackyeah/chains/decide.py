import os
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(api_key=os.getenv("OPENAI_APIKEY"), temperature=0.1)

decide_template = template = """
Dostajesz pytanie oraz zawartość HTML. Sprawdź, czy w tej zawartości znajdują się informacje, które odpowiadają na pytanie.

Pytanie: {question}

Zawartość HTML: {html_content}

Czy w zawartości HTML znajdują się informacje, które odpowiadają na pytanie? Odpowiedz tylko "tak" lub "nie".
"""


decide_prompt = PromptTemplate(
    input_variables=["question", "html_content"], template=decide_template
)

decide_chain = decide_prompt | llm


def decide(question: str, content):
    res = decide_chain.invoke({"question": question, "html_content": content})
    return res
