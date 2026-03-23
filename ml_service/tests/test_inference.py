import pytest
from unittest.mock import MagicMock
from app.model_inference import HFInference


@pytest.mark.asyncio
async def test_analyse_tweet_logic():
    # 1. SETUP MOCK
    # Create a fake engine and fake output
    mock_engine = MagicMock()
    mock_output = MagicMock()
    mock_output.outputs = [MagicMock(text="This is a test analysis.")]

    # Simulate the async generator behavior of vLLM
    async def mock_generator(*args, **kwargs):
        yield mock_output

    # Tell the mock engine to use our fake generator
    mock_engine.generate.side_effect = mock_generator

    # 2. INITIALIZE SERVICE
    # Inject the mock_engine directly! No @patch needed.
    service = HFInference(engine=mock_engine, model_id="test-model")

    # 3. TEST DATA
    tweet_data = {
        "text": "Breaking news: The sun is bright today.",
        "image_url": "http://example.com/sun.jpg",
    }

    # 4. EXECUTE
    result = await service.analyse_tweet(tweet_data)

    # 5. ASSERTIONS
    assert "analysis" in result
    assert result["analysis"] == "This is a test analysis."

    # Verify the engine was called with our prompt
    # Since we aren't patching, we check the mock directly
    args, kwargs = mock_engine.generate.call_args
    assert "Breaking news" in args[0]  # Check prompt string
