from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import edge_tts
import asyncio
import os
from config import DEFAULT_VOICE, DEFAULT_OUTPUT_FILE

app = FastAPI(title="Advanced Microsoft Edge TTS API")

# Enable CORS to allow browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def generate_tts(text: str, voice: str, output_file: str):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

@app.get("/")
def home():
    return {"message": "Welcome to Edge TTS API. Use /synthesize endpoint."}

@app.get("/synthesize")
async def synthesize(
    text: str = Query(..., description="Text to convert to speech"),
    voice: str = Query(DEFAULT_VOICE, description="Microsoft Edge voice name"),
):
    output_file = DEFAULT_OUTPUT_FILE

    try:
        await generate_tts(text, voice, output_file)
        return FileResponse(output_file, media_type="audio/mpeg", filename="output.mp3")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.on_event("shutdown")
def cleanup():
    if os.path.exists(DEFAULT_OUTPUT_FILE):
        os.remove(DEFAULT_OUTPUT_FILE)
