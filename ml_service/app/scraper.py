import httpx
from bs4 import BeautifulSoup


def scrape_tweet(url: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    with httpx.Client(headers=headers, follow_redirects=True) as client:
        response = client.get(url)
        if response.status_code != 200:
            return {}

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.find("meta", property="og:description")
        image = soup.find("meta", property="og:image")

        return {
            "text": text["content"] if text else "No text found",
            "image_url": image["content"] if image else None,
        }
