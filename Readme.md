# 🎙 AI Voice Agent with FastAPI

This project is a **multi-day development journey** to build an **AI-powered Voice Agent** using **FastAPI** as the backend framework.  
The Voice Agent is capable of **real-time voice interaction**, **speech synthesis**, and **websocket communication** between frontend and backend.  
The development was done in phases (Day 1, Day 2, Day 3) — each adding new functionalities and integrating different technologies.

---

## 📅 Day-wise Development Documentation

### **Day 1 – Basic FastAPI + Voice Agent Setup**
**Tech Stack:**
- **FastAPI** → Backend framework for creating APIs and handling requests
- **Uvicorn** → ASGI server to run FastAPI
- **OpenAI API** → For AI responses (text generation)
- **python-dotenv** → Manage environment variables securely

**Purpose:**
- Set up the basic FastAPI server
- Create API endpoints for AI interaction
- Load API keys from `.env`
- Establish the foundation for the voice assistant logic

---

### **Day 2 – Adding TTS (Text-to-Speech) and Audio Handling**
**Tech Stack:**
- **gTTS** → Convert AI text responses into audio
- **pydub** → Handle audio file conversion and processing

**Purpose:**
- Enable **speech synthesis** for AI responses
- Convert generated text into **MP3/WAV** audio formats
- Prepare audio responses for playback in the frontend

---

### **Day 3 – Frontend + WebSocket Integration**
**Tech Stack:**
- **jinja2** → Render HTML templates in FastAPI
- **websockets** → Real-time communication between client and server
- **aiofiles** → Handle asynchronous file operations

**Purpose:**
- Create a frontend interface for the voice assistant
- Use **WebSocket** for real-time request/response streaming
- Allow users to interact with the AI in real-time from a web browser

---

## 📦 Requirements
Install dependencies from the `requirements.txt` file:
```bash
pip install -r requirements.txt