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
    sub_image_url: str  # Added this field
    content: str

class NewspaperData(BaseModel):
    ticker_text: str
    articles: List[Article]

# Initialized database with the new structure
db = {
    "ticker_text": "مرحباً بكم في صحيفة الذكر",
    "articles": [
        {
            "category": "Education",
            "title": f"Feature Story {i}",
            "description": "Click to read more.",
            "image_url": "https://via.placeholder.com/400",
            "sub_image_url": "https://via.placeholder.com/600",
            "content": "This is the sub-article content."
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
    # Using .model_dump() is the modern Pydantic v2 approach
    db["articles"] = [a.model_dump() for a in data.articles]
    return {"message": "Success"}