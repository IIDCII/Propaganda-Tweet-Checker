from fastapi import FastAPI
from pydantic import BaseModel
from scraper import scrape_tweet
from model_inference import HFInference
from fastapi.concurrency import run_in_threadpool
from cache_model import download_model

app = FastAPI()

# TODO this model selection is currently hardcoded for now.
# Change so that it's modular for cascading in future versions

download_model()
model_id = "Qwen/Qwen2-VL-2B-Instruct"
engine = HFInference(model_id)


class TweetRequest(BaseModel):
    url: str


class AnalysisResponse(BaseModel):
    analysis: str
    status: str = "success"


@app.post("/analyze")
async def post_analysis(request: TweetRequest):
    tweet_data = await run_in_threadpool(scrape_tweet, request.url)

    if not tweet_data.get("text"):
        return {"analysis": "Error: Could not scrape tweet", "status": "failed"}

    output = await run_in_threadpool(engine.analyse_tweet, tweet_data)
    return output


@app.get("/metrics")
async def get_metrics():
    stats = engine.engine.get_stats()

    return {
        "running": stats.num_running,
        "waiting": stats.num_waiting,
        "gpu_cache_usage": stats.gpu_cache_usage,
    }
