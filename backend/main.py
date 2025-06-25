from fastapi import FastAPI, HTTPException, Body
from database import database, engine, metadata
import crud
import httpx
from schemas import CatCreate, CatUpdate, Cat, MissionCreate, Mission, TargetUpdate, Target

app = FastAPI()

metadata.create_all(engine)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Validação do breed com TheCatAPI
async def validate_breed(breed_name: str) -> bool:
    async with httpx.AsyncClient() as client:
        resp = await client
