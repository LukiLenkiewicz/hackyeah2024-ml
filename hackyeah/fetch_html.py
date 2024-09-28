import requests


def fetch_html(url):
    try:
        response = requests.get(url)

        response.raise_for_status()

        return response.text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
