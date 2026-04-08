import logging

import uvicorn
from fastapi import FastAPI

from src.db.pg import init_db
from src.shorted_url.routers import router as shorted_url_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="URL Shortener 3000")
app.include_router(shorted_url_router)


@app.on_event("startup")
async def on_startup():
    await init_db()


if __name__ == "__main__":
    # This allows you to right-click 'main.py' and select 'Debug'
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)