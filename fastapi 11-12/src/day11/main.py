from fastapi import FastAPI


app = FastAPI(
    title="GenAI Day 11-12 API",
    description="FastAPI application for Day 11-12",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Day 11 API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }