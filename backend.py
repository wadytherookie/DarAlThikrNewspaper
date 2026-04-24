import os
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from pymongo import MongoClient

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB (Replace with your actual string!)
MONGO_URI = "mongodb+srv://therookiebeer_db_user:<db_password>@cluster0.bmo0g8u.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["newspaper_db"]
collection = db["articles"]

class Article(BaseModel):
    category: str
    title: str
    description: str
    image_url: str
    sub_image_1: Optional[str] = ""
    sub_image_2: Optional[str] = ""
    sub_image_3: Optional[str] = ""
    sub_image_4: Optional[str] = ""
    content: str

class NewspaperData(BaseModel):
    ticker_text: str
    articles: List[Article]

@app.get("/status")
def get_status():
    data = collection.find_one({"_id": "main_config"})
    if not data:
        return {"ticker_text": "مرحباً بكم في صحيفة الذكر", "articles": []}
    data.pop('_id', None) # Remove MongoDB ID before sending to frontend
    return data

@app.post("/update")
def update_portal(data: NewspaperData, x_admin_token: str = Header(None)):
    if x_admin_token != "DarAlThikr_Secret_2026":
        raise HTTPException(status_code=403, detail="Invalid Token")
    collection.replace_one({"_id": "main_config"}, data.model_dump(), upsert=True)
    return {"message": "Success"}