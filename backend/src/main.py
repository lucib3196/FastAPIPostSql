from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.src.db import create_db_and_tables
from backend.src.routes.pokemon import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
