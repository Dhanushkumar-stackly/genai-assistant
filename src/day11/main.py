
from fastapi import FastAPI


# Create the FastAPI application
app = FastAPI()


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Day 11 API is running"
    }
