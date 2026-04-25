from fastapi import FastAPI
from src.api.routes import router

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

app.include_router(router)


@app.get("/")
def root():
    return {"message": "PatternBuster API running 🚀"}