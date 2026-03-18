import requests
import os
import time

# Use Environment Variables with Docker service names as defaults
API_URL = os.getenv("TARGET_API_URL", "http://api:3000")


def test_full_propaganda_pipeline():
    """Test: Frontend Request -> Axum API -> FastAPI ML -> DB"""
    payload = {"tweet_text": "This is a test propaganda tweet."}

    # 1. Hit the Axum API
    response = requests.post(f"{API_URL}/check", json=payload)

    assert response.status_code == 200
    data = response.json()

    # 2. Verify the ML service returned a classification
    assert "is_propaganda" in data
    assert "confidence" in data

    # 3. (Optional) Check the DB directly to ensure the entry was cached
    # This ensures your 'lifetime' logic is working.
