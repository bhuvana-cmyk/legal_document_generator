from fastapi import FastAPI
from routes import router

app = FastAPI(title="LegalEase")

@app.get("/")
def home():
    return {"message": "LegalEase API is running"}

app.include_router(router)
