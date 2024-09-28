import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict


# Helper function to get the base URL (scheme + domain)
def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


# Helper function to get all sub-URLs from a given page asynchronously
async def fetch_content(session, url):
    try:
        async with session.get(url) as response:
            if response.status != 200:
                return None, None
            content = await response.text()  # Get the HTML content of the page
            return content, url
    except Exception as e:
        return None, None  # Return None in case of an exception


# Helper function to parse URLs from the HTML content
def parse_urls(url, content, base_url):
    soup = BeautifulSoup(content, "html.parser")
    sub_urls = set()

    for a_tag in soup.find_all("a", href=True):
        link = urljoin(url, a_tag["href"])  # Resolve relative URLs to absolute ones
        parsed_link = urlparse(link)

        # Check if the sub-URL has the same base URL as the main URL
        if f"{parsed_link.scheme}://{parsed_link.netloc}" == base_url:
            sub_urls.add(link)

    return sub_urls, soup.get_text()


async def gather_sub_urls(session, urls, base_url):
    tasks = [fetch_content(session, url) for url in urls]
    results = await asyncio.gather(*tasks)

    # Only return URLs that match the base URL
    return [
        (content, url)
        for content, url in results
        if content and get_base_url(url) == base_url
    ]


async def async_create_url_graph(url: str, depth: int):
    base_url = get_base_url(url)  # Extract the base URL of the main URL
    graph = defaultdict(lambda: {"content": "", "sub_urls": {}})

    # Limit the number of concurrent requests
    sem = asyncio.Semaphore(20)  # Limits concurrency to avoid overloading the server

    async with aiohttp.ClientSession() as session:

        async def async_traverse(url, depth):
            if depth == 0 or url in graph:
                return

            async with sem:  # Ensure no more than `sem` tasks are running concurrently
                content, fetched_url = await fetch_content(session, url)
                if content is None:
                    return

                # Parse URLs and content asynchronously
                sub_urls, page_content = parse_urls(url, content, base_url)

                # Append to graph concurrently
                graph[url]["content"] = page_content
                graph[url]["sub_urls"] = {sub_url: {} for sub_url in sub_urls}

                if depth > 1:
                    # Recursively process all sub-URLs with decreased depth
                    tasks = [async_traverse(sub_url, depth - 1) for sub_url in sub_urls]
                    await asyncio.gather(*tasks)

        await async_traverse(url, depth)
    return graph


# Running the graph creation function with asyncio
def create_url_graph(url: str, depth: int):
    return asyncio.run(async_create_url_graph(url, depth))
