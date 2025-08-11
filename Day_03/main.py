import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import httpx

# Load environment variables
load_dotenv()
MURF_API_KEY = os.getenv("MURF_API_KEY")

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Static + templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class TTSRequest(BaseModel):
    text: str
    voiceId: str
    format: str = "mp3"

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/voices")
async def get_voices():
    """Fetch available voices from Murf API."""
    if not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "MURF_API_KEY not set"})

    url = "https://api.murf.ai/v1/speech/voices"
    headers = {"api-key": MURF_API_KEY, "Accept": "application/json"}

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(url, headers=headers)
        return JSONResponse(status_code=r.status_code, content=r.json())
    except Exception as e:
        logging.exception("Error fetching voices")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/generate-tts")
async def generate_tts(payload: TTSRequest):
    """Generate speech from text using Murf API."""
    if not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "MURF_API_KEY not set"})

    url = "https://api.murf.ai/v1/speech/generate"
    headers = {
        "Accept": "application/json",
        "api-key": MURF_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, headers=headers, json=payload.dict())
        data = r.json()

        if r.status_code == 200 and "audioFile" in data:
            return {"audio_url": data["audioFile"]}
        else:
            return JSONResponse(status_code=502, content={"error": data})
    except Exception as e:
        logging.exception("Error generating audio")
        return JSONResponse(status_code=500, content={"error": str(e)})