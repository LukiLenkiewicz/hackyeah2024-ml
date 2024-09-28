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
Does this text fully and exhaustively provide all the necessary, detailed, and specific information required for the end user to answer the question: {question} with complete certainty, without any ambiguity or need for further clarification?
 
Please evaluate whether the answer is explicitly and directly present, including every critical detail needed. If any part of the required information is missing, incomplete, vague, or implied rather than clearly stated, explain why the information is insufficient.

Return the output in JSON format with two keys:
1. "reasoning": a detailed explanation of why the content is or is not fully sufficient.
2. "answer": a boolean that is true only if the content provides a 100% complete and unambiguous answer.


Website Content:
```
{html_content}
```
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
