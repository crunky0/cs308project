import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import database

from stock_endpoints import router as stock_router  # Import the router
from user_endpoints import router as user_router  # Import the router
from rating_endpoints import router as rating_router
from categorysearch_endpoints import router as category_search_router
from card_endpoints import router as card_router


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

# Include the user router

app.include_router(stock_router)
app.include_router(user_router)
app.include_router(rating_router)
app.include_router(category_search_router)
app.include_router(card_router)
