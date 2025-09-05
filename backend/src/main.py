from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db import create_db_and_tables
from src.routes.pokemon import router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

@asynccontextmanager
async def lifespan(_: FastAPI):
    print("Creating tables")
    create_db_and_tables()
    print("Complete")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for prod
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# TEMP: print the routes to verify methods/paths
for r in app.routes:
    if isinstance(r, APIRoute):
        print("ROUTE:", r.path, r.methods)
