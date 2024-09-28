import requests
from bs4 import BeautifulSoup

cookies = dict(language="pl_PL")


def get_website_text(url, cookies=None):
    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, "html.parser")
    except (requests.RequestException, Exception) as e:
        print(f"Failed to access {url}: {e}")
        return

    # Extract the text from the <body> tag
    body = soup.body
    if body is None:
        return "No body content found."

    # Get the text content, stripping extra spaces and newlines
    website_text = body.get_text(separator="\n", strip=True)
    return website_text


# Example usage


# Example usage
# url = "https://example.com"
# content = get_website_content(url)
# print(content)
