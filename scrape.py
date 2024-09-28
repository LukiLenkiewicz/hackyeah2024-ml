from scrapegraphai.graphs import SmartScraperGraph

graph_config = {
    "llm": {
        "model": "ollama/llama3.1",
        "base_url": "http://localhost:11434",
    }}

smart_scraper_graph = SmartScraperGraph(
    prompt="Na jakim adresie url zapłacę PIT?",
    source="https://wroclaw.sa.gov.pl/",
    config=graph_config
)

result = smart_scraper_graph.run()
print(result)
