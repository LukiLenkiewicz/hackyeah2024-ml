import os
import json
from dotenv import load_dotenv
import concurrent.futures

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from hackyeah.chains.decide import decide
from hackyeah.chains.rank_urls import get_urls
from hackyeah.get_website_text import get_website_text
from hackyeah.general_scraping import find_subsites_with_info


load_dotenv()

openai_api_key = os.getenv("OPENAI_APIKEY")

question = "Jakie są szpitale w Krakowie?"


chat = ChatOpenAI(model="gpt-3.5-turbo-1106", api_key=openai_api_key, temperature=0)

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


prompt_template = PromptTemplate.from_template(
    "Twoim zadaniem jest analiza strony pod adresem {url} na podstawie poniższego kodu HTML. Użytkownik zadał następujące pytanie: {question}. Korzystając ze struktury HTML, wyjaśnij krok po kroku, jak użytkownik może wykonać tę akcję na stronie, odnosząc się do konkretnych elementów (np. formularzy, przycisków) w kodzie HTML.\n\nHTML:\n{html}"
)


class HackYeahClient:
    def __init__(self, url, chain, id):
        self.url = url
        self.chain = chain
        self.id = id

    def find_url(self, question):
        # Get content from the base URL and make the decision
        url = self.url
        content = get_website_text(url)
        payload = decide(question=question, content=content)
        decision = json.loads(payload)["answer"]
        print(decision)

        # If the decision is True, return the result
        if decision:
            return self.chain.invoke(
                {
                    "input": prompt_template.format(
                        url=url, question=question, html=content
                    )
                },
                {"configurable": {"session_id": self.id}},
            )

        # If decision is False, find subsites and search in parallel
        sub_urls = find_subsites_with_info(url)
        relevant_urls = get_urls(question, sub_urls)

        def process_url(sub_url):
            """Helper function to process each URL in parallel."""
            content = get_website_text(sub_url)
            payload = decide(question=question, content=content)
            decision = json.loads(payload)["answer"]
            if decision:
                return self.chain.invoke(
                    {
                        "input": prompt_template.format(
                            url=sub_url, question=question, html=content
                        )
                    },
                    {"configurable": {"session_id": self.id}},
                )

            else:
                # Recursively search on this URL if decision is False
                return self.find_url(sub_url, question)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(process_url, sub_url): sub_url
                for sub_url in relevant_urls
            }
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    return result

        return None
