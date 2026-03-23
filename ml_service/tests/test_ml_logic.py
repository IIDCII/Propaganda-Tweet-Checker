import pytest
from unittest.mock import MagicMock, patch
from app.model_inference import HFInference
from app.scraper import scrape_tweet


@pytest.mark.asyncio
@patch("vllm.AsyncLLMEngine.from_engine_args")
async def test_analyse_tweet_formatting(mock_from_args):
    # 1. Setup the Mock Engine
    mock_engine = MagicMock()
    mock_from_args.return_value = mock_engine

    # 2. Mock the async generator for 'generate'
    mock_output = MagicMock()
    mock_output.outputs = [MagicMock(text="Propaganda")]

    async def mock_gen(*args, **kwargs):
        yield mock_output

    # This is the "Camera" that records the call
    mock_engine.generate.side_effect = mock_gen

    # 3. Execution
    engine_wrapper = HFInference(model_id="test-model", engine=mock_engine)
    tweet_data = {"text": "Target Text", "image_url": None}
    await engine_wrapper.analyse_tweet(tweet_data)

    # 4. Verification using call_args
    # Now .generate is a Mock object, so it HAS call_args
    args, kwargs = mock_engine.generate.call_args

    # args[0] is the 'prompt' string passed to generate()
    assert "Target Text" in args[0]
    assert "propaganda" in args[0].lower()
