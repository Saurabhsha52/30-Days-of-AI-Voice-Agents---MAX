# main.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

class TextRequest(BaseModel):
    text: str

@app.post("/generate-audio")
async def generate_audio_url(text_data: TextRequest):
    api_key = os.getenv("MURF_API_KEY")
    if not api_key:
        return {"error": "API key not found."}, 500
    
    murf_api_url = "https://api.murf.ai/v1/generate"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text_data.text,
        "voice_id": "en-US-amara" 
    }
    
    try:
        response = requests.post(murf_api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        audio_url = response.json().get("audio_url")

        if audio_url:
            return {"audio_url": audio_url}
        else:
            return {"error": "Failed to get audio URL from Murf API"}, 500

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}, 500