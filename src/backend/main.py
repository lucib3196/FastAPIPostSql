from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List, Annotated
from src.backend.db import create_db_and_tables
from src.backend.routes.pokemon import router




@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield
    
app = FastAPI(lifespan=lifespan)
app.include_router(router)