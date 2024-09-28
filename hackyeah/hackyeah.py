import os
from dotenv import load_dotenv
from scrapegraphai.graphs import SmartScraperGraph

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from fetch_html import fetch_html

load_dotenv()

openai_api_key = os.getenv("OPENAI_APIKEY")

graph_config = {
    "llm": {
        "api_key": openai_api_key,
        "model": "openai/gpt-4o-mini",
    },
    "verbose": True,
    "headless": True,
}

question = "Na jakim adresie url zapłacę PIT?"

smart_scraper_graph = SmartScraperGraph(
    prompt=question,
    source="https://wroclaw.sa.gov.pl/",
    config=graph_config,
)

result = smart_scraper_graph.run()
url = result["url"]


chat = ChatOpenAI(
    model="gpt-3.5-turbo-1106",
    api_key=openai_api_key,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Jesteś asystentem nawigacji po stronach internetowych. Na podstawie adresu URL strony, jej kodu HTML oraz pytania użytkownika, podaj adres URL i jasne, zwięzłe kroki, jak wykonać żądaną akcję, odnosząc się do odpowiednich elementów HTML.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

chain = prompt | chat

demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

hack_yeah_chain = RunnableWithMessageHistory(
    chain,
    lambda session_id: demo_ephemeral_chat_history_for_chain,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# example usage

# prompt_template = PromptTemplate.from_template(
#     "Twoim zadaniem jest analiza strony pod adresem {url} na podstawie poniższego kodu HTML. Użytkownik zadał następujące pytanie: {question}. Korzystając ze struktury HTML, wyjaśnij krok po kroku, jak użytkownik może wykonać tę akcję na stronie, odnosząc się do konkretnych elementów (np. formularzy, przycisków) w kodzie HTML.\n\nHTML:\n{html}"
# )

# formatted_prompt = prompt_template.format(
#     url=url, question=question, html=fetch_html(url)
# )

# nl_ans = chain_with_message_history.invoke(
#     {"input": formatted_prompt}, {"configurable": {"session_id": "unused"}}
# )
# print(nl_ans.content)
