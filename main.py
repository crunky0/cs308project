import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from databases import Database
from passlib.context import CryptContext
from db import database
from user_endpoints import router as user_router  # Import the router

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FastAPI app initialization
app = FastAPI()

# Connect to the database when the app starts
@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()

# Disconnect from the database when the app shuts down
@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

app.include_router(user_router)