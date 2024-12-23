import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import database
from fastapi.middleware.cors import CORSMiddleware
from product_manager_endpoints import manager_router


# FastAPI app initialization with lifespan context
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    if not database.is_connected:
        await database.connect()
    yield  # This yields control to the application during its lifespan
    # Shutdown logic
    if database.is_connected:
        await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(manager_router)
