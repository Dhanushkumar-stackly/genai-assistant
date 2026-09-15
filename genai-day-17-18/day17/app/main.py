from fastapi import FastAPI

from .voice_input import router as voice_router


app = FastAPI(
    title="GenAI Assistant - Day 17",
)


app.include_router(voice_router)


@app.get("/")
def root():
    return {
        "message": (
            "Day 17 audio input path is running"
        )
    }