import pytest
from unittest.mock import patch, MagicMock
from app.scraper import scrape_tweet


def test_scrape_tweet_structure():
    mock_html = """
    <html>
        <meta property="og:description" content="Modular AI is great!">
        <meta property="og:image" content="https://example.com/ai.png">
    </html>
    """

    with patch("httpx.Client.get") as mock_get:
        mock_get.return_value = MagicMock(status_code=200, text=mock_html)

        result = scrape_tweet("https://x.com/status/123")

        assert result["text"] == "Modular AI is great!"
        assert result["image_url"] == "https://example.com/ai.png"
