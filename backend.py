from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# This is the "Security Guard" that lets your HTML talk to Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ADMIN_TOKEN = "DarAlThikr_Secret_2026"

class Article(BaseModel):
    category: str
    title: str
    description: str  # Changed from 'content' to match the HTML
    image_url: str    # Changed from 'image' to match the HTML

class NewspaperData(BaseModel):
    ticker_text: str
    is_active: bool   # Changed from 'is_submissions_active' to match the HTML
    articles: List[Article]


db = {
    "ticker_text": "Welcome to the North.ai Portal!",
    "is_active": False,
    "articles": [
        {"category": "News", "title": f"Story {i}", "description": "Pending update...", "image_url": "https://via.placeholder.com/400"} 
        for i in range(1, 7)
    ]
}

@app.get("/status")
def get_status():
    return db

@app.post("/update")
def update_portal(data: NewspaperData, x_admin_token: str = Header(None)):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # We update the global 'db' variable
    db["ticker_text"] = data.ticker_text
    db["is_active"] = data.is_active
    db["articles"] = [a.dict() for a in data.articles]
    
    return {"message": "Newspaper Updated!"}