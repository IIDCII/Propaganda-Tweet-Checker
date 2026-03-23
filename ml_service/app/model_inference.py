from vllm import SamplingParams
import uuid


class HFInference:
    def __init__(self, model_id: str, engine):
        self.model_id = model_id
        self.engine = engine

    async def analyse_tweet(self, tweet_data: dict) -> dict:
        request_id = str(uuid.uuid4())
        prompt = f"tell me if the following tweet is propaganda or not \n {tweet_data['text']}"
        sampling_params = SamplingParams(temperature=0.0, max_tokens=512)

        results_generator = self.engine.generate(prompt, sampling_params, request_id)

        final_output = None

        async for request_output in results_generator:
            final_output = request_output
            return {"analysis": final_output.outputs[0].text}

        return {"analysis": "ERROR: Analysis could not complete"}
