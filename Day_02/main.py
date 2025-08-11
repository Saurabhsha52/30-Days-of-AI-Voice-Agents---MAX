# main.py (improved debugging + /voices endpoint)
import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import httpx

load_dotenv()
MURF_API_KEY = os.getenv("MURF_API_KEY")

logging.basicConfig(level=logging.INFO)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class TTSRequest(BaseModel):
    text: str
    voiceId: str = "en-US-natalie"   # default; replace if needed
    format: str = "mp3"

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/voices")
async def get_voices():
    if not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "MURF_API_KEY not set"})
    url = "https://api.murf.ai/v1/speech/voices"
    headers = {"api-key": MURF_API_KEY, "Accept": "application/json"}
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(url, headers=headers)
        logging.info("GET /v1/speech/voices -> %s", r.status_code)
        try:
            data = r.json()
        except Exception:
            data = {"raw": r.text}
        return JSONResponse(status_code=r.status_code, content=data)
    except Exception as e:
        logging.exception("Error fetching voices")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/generate-tts")
async def generate_tts(payload: TTSRequest):
    if not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "MURF_API_KEY not set"})
    url = "https://api.murf.ai/v1/speech/generate"
    headers = {
        "Accept": "application/json",
        "api-key": MURF_API_KEY,
        "Content-Type": "application/json",
    }
    body = payload.dict()
    logging.info("Calling Murf generate with body: %s", {k:v for k,v in body.items() if k != "text"})
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, headers=headers, json=body)
        logging.info("Murf response status: %s", r.status_code)
        logging.info("Murf response body: %s", r.text[:1000])  # truncated log
        try:
            data = r.json()
        except Exception:
            data = {"raw": r.text}
        if r.status_code == 200:
            audio_url = data.get("audioFile") or data.get("audio_file") or data.get("audioUrl")
            return {"status": "ok", "audio_url": audio_url, "raw": data}
        else:
            # return murf error back to frontend for debugging (safe since it doesn't include API key)
            return JSONResponse(status_code=502, content={"error": "Murf API error", "status_code": r.status_code, "body": data})
    except httpx.TimeoutException:
        logging.exception("Timeout contacting Murf")
        return JSONResponse(status_code=504, content={"error": "timeout contacting Murf"})
    except Exception as e:
        logging.exception("Unhandled exception")
        return JSONResponse(status_code=500, content={"error": str(e)})