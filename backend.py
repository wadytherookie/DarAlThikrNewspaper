from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 1. THE SECURITY GUARD (CORS)
# This MUST be here so your static HTML site can talk to Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ADMIN_TOKEN = "DarAlThikr_Secret_2026"

# 2. DATA MODELS
class Article(BaseModel):
    category: str
    title: str
    description: str
    image_url: str

class NewspaperData(BaseModel):
    ticker_text: str
    is_active: bool
    articles: List[Article]

# 3. THE DATABASE (Stored in RAM)
# Initialized with 6 placeholders
db = {
    "ticker_text": "Welcome to the Control Center!",
    "is_active": False,
    "articles": [
        {
            "category": "News", 
            "title": f"Story {i}", 
            "description": "Waiting for update from Control Center...", 
            "image_url": "https://via.placeholder.com/400"
        } for i in range(1, 7)
    ]
}

# 4. THE ROUTES
@app.get("/status")
def get_status():
    return db

@app.post("/update")
def update_portal(data: NewspaperData, x_admin_token: str = Header(None)):
    # Check if the token sent from dashboard.html matches ours
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid Token")
    
    # Update the global 'db'
    db["ticker_text"] = data.ticker_text
    db["is_active"] = data.is_active
    db["articles"] = [a.dict() for a in data.articles]
    
    return {"message": "Newspaper Updated Successfully!"}