from pydantic import BaseModel
from langchain_openai import ChatOpenAI


class RankedURLs(BaseModel):
    urls: list[str]


class UtilityCheck(BaseModel):
    useful: bool


llm = ChatOpenAI(temperature=0.1)
structured_llm = llm.with_structured_output(RankedURLs)
utility_check_llm = llm.with_structured_output(UtilityCheck)
