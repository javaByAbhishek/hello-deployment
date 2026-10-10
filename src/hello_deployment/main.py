import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from google import genai
from pydantic import BaseModel, Field

app = FastAPI()
static_dir = Path(__file__).parent / "static"


class PromptRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=1000)


@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI!"}


@app.post("/api/generate")
def generate(request: PromptRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set.")

    model = os.getenv("GOOGLE_LLM_MODEL", "gemini-3.1-flash-lite")

    try:
        client = genai.Client(api_key=api_key)
        result = client.models.generate_content(
            model=model,
            contents=request.prompt,
        )
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Gemini request failed. Check the FastAPI terminal for details.",
        )

    return {"response": result.text or ""}


@app.get("/")
def home():
    return FileResponse(static_dir / "index.html")