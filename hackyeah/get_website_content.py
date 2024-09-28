import requests


def get_website_content(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.text
        else:
            return f"Error: Received status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


# Example usage
# url = "https://example.com"
# content = get_website_content(url)
# print(content)
