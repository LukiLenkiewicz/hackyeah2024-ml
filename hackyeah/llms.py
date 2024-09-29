from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from scrapegraphai.graphs import SmartScraperGraph
import json
import os

# Assuming the templates are defined as previously discussed
PROMPT_EXTRACT_RELEVANT_SUBSITES_TEMPLATE = """
    [QUESTION] {user_question}
    [WEBSITES] {list_of_websites}
    """

PROMPT_CLASSIFY_RELEVANCE_TEMPLATE = """
    {text}

    Does this text contain comprehensive and specific information to answer the question: '{user_question}' Please provide details on whether the answer is directly present, and if not, explain why the information is insufficient for what the user is seeking to find. Then answer TRUE or FALSE in new line.
    """

# Function to classify relevance using OpenAI
def classify_relevance(user_question, text):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    # prompt = ChatPromptTemplate.from_template(PROMPT_CLASSIFY_RELEVANCE_TEMPLATE)
    # prompt = prompt.format(user_question=user_question, text=text)
    # response = llm.invoke(prompt).content
    prompt = ChatPromptTemplate.from_messages(
        [
            ("human", PROMPT_CLASSIFY_RELEVANCE_TEMPLATE),
        ]
    )
    chain = prompt | llm
    response = chain.invoke(
        {
            "user_question": user_question,
            "text": text,
        }
    ).content

    return response

# Function to extract relevant subsites using OpenAI
def extract_relevant_subsites(list_of_websites, user_question):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    # prompt = ChatPromptTemplate.from_template(PROMPT_EXTRACT_RELEVANT_SUBSITES_TEMPLATE)
    # prompt = prompt.format(user_question=user_question, list_of_websites=list_of_websites)
    # response = llm.invoke(prompt).content
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a professional search ranking tool, which enables user to input a list of websites with short descriptions and a search query. Your role is to return a list of URLs to websites by sorting them by relevance to the given question. Return only these website than in your opinion may contain information which will be able to provide answer to user question.
                Return ONLY the JSON containing websites SORTED BY RELEVANCE TO THE USER QUESTION. Don't write any additional text or comments. Don't explain your resoning. Don't define any additional structures."""
            ),
            ("human", PROMPT_EXTRACT_RELEVANT_SUBSITES_TEMPLATE),
        ]
    )
    chain = prompt | llm
    response = chain.invoke(
        {
            "user_question": user_question,
            "list_of_websites": list_of_websites,
        }
    ).content
    
    cleaned_output = response.replace("json", "").replace("```", "").strip()

    try:
        # Parse the cleaned JSON string
        return json.loads(cleaned_output)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return []

def chat_with_website(url, question):
    graph_config = {
        "llm": {
            "api_key": os.environ.get("OPENAI_API_KEY"),
            "model": "openai/gpt-4o-mini",
        },
        "verbose": False,
        "headless": True,
    }

    # Create the SmartScraperGraph instance
    smart_scraper_graph = SmartScraperGraph(
        prompt=f"Find some information that will help me answer the question: {question}. Return retrieved information in plain text. If user asks for instructions to complete a task, provide a step-by-step guide, with each step in a new line.",
        source=url,
        config=graph_config
    )

    # Run the pipeline
    result = smart_scraper_graph.run()
    return result