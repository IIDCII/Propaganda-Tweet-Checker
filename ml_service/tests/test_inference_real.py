import pytest
import os
from vllm import AsyncLLMEngine, AsyncEngineArgs
from app.model_inference import HFInference


# This "mark" allows us to skip this test during quick local runs
@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_inference_qwen():
    # 1. SETUP REAL ENGINE
    # We use a small max_model_len to save GPU memory during testing
    model_id = "Qwen/Qwen2-VL-2B-Instruct"
    engine_args = AsyncEngineArgs(
        model="Qwen/Qwen2-VL-2B-Instruct",
        limit_mm_per_prompt={"image": 1},
        trust_remote_code=True,
        max_model_len=1024,
        device="cuda",
        gpu_memory_utilization=0.8,
        hf_overrides={"rope_scaling": {"type": "mrope", "mrope_section": [16, 24, 56]}},
    )

    engine = AsyncLLMEngine.from_engine_args(engine_args)

    # 2. INITIALIZE SERVICE
    service = HFInference(engine=engine, model_id=model_id)

    # 3. REAL TEST DATA
    tweet_data = {
        "text": "The government is lying to you about the moon! Join the resistance now!",
    }

    # 4. EXECUTE (This will take a few seconds)
    result = await service.analyse_tweet(tweet_data)

    # 5. ASSERTIONS
    assert "analysis" in result
    print(f"\nModel Output: {result['analysis']}")

    # We check for basic string length to ensure it actually generated text
    print(f"Analysis output:\n{result['analysis']}")
    assert len(result["analysis"])
