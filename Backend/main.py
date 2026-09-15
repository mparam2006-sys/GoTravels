from fastapi import FastAPI

app = FastAPI(title="GoTravels API")


@app.get("/")
def home():
    return {
        "message": "Welcome to GoTravels API"
    }