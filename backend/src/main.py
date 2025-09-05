from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db import create_db_and_tables
from src.routes.pokemon import router
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
app.include_router(router)
