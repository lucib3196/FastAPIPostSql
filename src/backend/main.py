from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List, Annotated
from routes.pokemon import router
from backend.db import create_db_and_tables




@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield
    
app = FastAPI(lifespan=lifespan)
app.include_router(router)