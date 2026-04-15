import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.db.pg import init_db
from src.shorted_url.routers import router as shorted_url_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="URL Shortener 3000",
    lifespan=lifespan
)

app.include_router(shorted_url_router)


if __name__ == "__main__":
    # This allows you to right-click 'main.py' and select 'Debug'
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)