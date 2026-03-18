from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "ML Service is running", "model": "Propaganda-Cascade-v1"}


@app.post("/predict")
def predict(data: dict):
    # Placeholder for your cascading ML logic
    return {"is_propaganda": False, "confidence": 0.99}
