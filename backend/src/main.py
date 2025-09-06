from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from src.db import create_db_and_tables
from src.routes.pokemon import router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from pathlib import Path


@asynccontextmanager
async def lifespan(_: FastAPI):
    print("Creating tables")
    create_db_and_tables()
    print("Complete")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
origins = [
    "http://localhost:5173",  # Vite dev
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/debug/images")
def list_images():
    print("Images")
    if not IMAGES_DIR.exists():
        raise HTTPException(500, f"Not found: {IMAGES_DIR}")
    return [p.name for p in IMAGES_DIR.iterdir() if p.is_file()]

IMAGES_DIR = Path(__file__).resolve().parent / "images"

app.mount(
    "/images",
    StaticFiles(directory=IMAGES_DIR),  # no need for html=True here
    name="images",
)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

