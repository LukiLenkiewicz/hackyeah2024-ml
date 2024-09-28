import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel

# Load API key from environment variable
load_dotenv()

model = ChatOpenAI(temperature=0, api_key=os.getenv("OPENAI_APIKEY"))


# Define the structure for the output using Pydantic
class Decision(BaseModel):
    reasoning: str
    answer: bool  # Using a boolean value instead of a string


# Wrap the LLM with structured output that conforms to the Decision schema
structured_llm = model.with_structured_output(Decision)

# Template to ask whether the content sufficiently answers the question
decide_template = """
Does this text contain comprehensive and specific information for the end user to answer the question: {question}?
Please provide details on whether the answer is directly present, and if not, explain why the information is insufficient.

Return the output in JSON format with two keys:
1. "reasoning": a string explaining the reasoning.
2. "answer": a boolean that is either true or false.

Website Content:
{html_content}

"""

# Create the prompt template from the above decide_template
decide_prompt = PromptTemplate.from_template(decide_template)

# Define the chain that processes the input using the structured LLM
decide_chain = decide_prompt | structured_llm


def decide(question: str, content: str):
    # Invoke the chain with formatted prompt and session history
    res = decide_chain.invoke({"question": question, "html_content": content})

    # Return the structured result in JSON format
    return res.json()
