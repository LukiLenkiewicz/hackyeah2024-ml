# EasyTalk - HackYeah 2024 project

This repository contains the implementation of EasyTalk, a project submitted for the Open Task: Artificial Intelligence at HackYeah 2024. EasyTalk is an AI-powered tool that enables seamless information retrieval from any website through a chatbot-like interface. By combining web scrapers with LLM capabilities, EasyTalk checks if a user's question can be answered from the starting page, and explores subsites if needed, prioritizing these with higher relevance to given question. Once the answer is found, EasyTalk retrieves and formats it in a suitable way, e.g. providing a step-by-step list when user asks for instructions.

## Running the project locally (Python 3.11)

Clone the repository:
```
git clone git@github.com:LukiLenkiewicz/hackyeah2024-ml.git
```

Install required packages:
```
cd hackheah2024-ml
pip install .
```

Create `.env` file and put your OpenAI API key in it e.g.:
```
OPENAI_API_KEY = "<your api key>"
```

Run the application:
```
python -m streamlit run scripts/app.py
```
