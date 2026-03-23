from contextlib import asynccontextmanager
from fastapi import FastAPI
from vllm import AsyncLLMEngine, AsyncEngineArgs
from app.model_inference import HFInference
from app.scraper import scrape_tweet

# 1. This dict will hold our "global" resources
ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    # Load the heavy engine once

    engine_args = AsyncEngineArgs(
        model="Qwen/Qwen2-VL-2B-Instruct",
        limit_mm_per_prompt={"image": 1},
        trust_remote_code=True,
        max_model_len=1024,
        device="cuda",
        gpu_memory_utilization=0.8,
        hf_overrides={"rope_scaling": {"rope_type": "default"}},
    )
    engine = AsyncLLMEngine.from_engine_args(engine_args)

    # Inject the engine into our service
    ml_models["inference_service"] = HFInference(
        engine=engine, model_id="propaganda-v1"
    )

    yield  # The app runs and handles requests here

    # --- SHUTDOWN ---
    # Clean up resources (like GPU memory) if needed
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.post("/analyze")
async def analyze(tweet_url: str):
    tweet_data = scrape_tweet(tweet_url)
    result = await ml_models["inference_service"].analyse_tweet(tweet_data)
    return result
