from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ADMIN_TOKEN = "DarAlThikr_Secret_2026"

class Article(BaseModel):
    category: str
    title: str
    description: str
    image_url: str
    content: str  # <--- NEW: For the "extra info" sub-article

class NewspaperData(BaseModel):
    ticker_text: str
    articles: List[Article]

db = {
    "ticker_text": "Welcome to The Al-Thikr Times.",
    "articles": [
        {
            "category": "Education", 
            "title": f"Feature Story {i}", 
            "description": "Click to read more about this update.", 
            "image_url": "https://via.placeholder.com/400",
            "content": "This is the extra information that appears when you click the article."
        } for i in range(1, 7)
    ]
}

@app.get("/status")
def get_status():
    return db

@app.post("/update")
def update_portal(data: NewspaperData, x_admin_token: str = Header(None)):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid Token")
    
    db["ticker_text"] = data.ticker_text
    db["articles"] = [a.dict() for a in data.articles]
    return {"message": "Success"}