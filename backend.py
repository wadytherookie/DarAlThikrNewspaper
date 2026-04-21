import json
import os
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ADMIN_TOKEN = "DarAlThikr_Secret_2026"
DATA_FILE = "newspaper_data.json"

class Article(BaseModel):
    category: str
    title: str
    description: str
    image_url: str
    # Updated to hold 4 sub-images
    sub_image_1: Optional[str] = ""
    sub_image_2: Optional[str] = ""
    sub_image_3: Optional[str] = ""
    sub_image_4: Optional[str] = ""
    content: str

class NewspaperData(BaseModel):
    ticker_text: str
    articles: List[Article]

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "ticker_text": "مرحباً بكم في صحيفة الذكر",
            "articles": [{
                "category": "عام", "title": "عنوان", "description": "وصف", 
                "image_url": "", "sub_image_1": "", "sub_image_2": "", 
                "sub_image_3": "", "sub_image_4": "", "content": ""
            } for _ in range(6)]
        }
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"ticker_text": "خطأ في البيانات", "articles": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.get("/status")
def get_status():
    return load_data()

@app.post("/update")
def update_portal(data: NewspaperData, x_admin_token: str = Header(None)):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid Token")
    
    # Save the updated data structure
    save_data(data.model_dump())
    return {"message": "Success"}