from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()
static_dir = Path(__file__).parent / "static"


@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI!"}


@app.get("/")
def home():
    return FileResponse(static_dir / "index.html")