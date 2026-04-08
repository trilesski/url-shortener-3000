import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.helpers import async_encode_base64
from src.db.pg import get_session as get_pg_session
from src.shorted_url.dao import ShortedUrlDAO
from src.shorted_url.models import ShortedUrl
from src.shorted_url.schemas import ShortenRequest, ShortenResponse, StatsResponse


router = APIRouter()
logger = logging.getLogger()


@router.post("/shorten", response_model=ShortenResponse)
async def shorten(req: ShortenRequest, db: AsyncSession = Depends(get_pg_session)):
    short_id = await async_encode_base64(str(req.url), max_len=10)
    shorted_url, is_created = await ShortedUrlDAO.get_or_create(db, original_url=str(req.url), short_id=short_id)

    logger.info(f"Shortened url: {shorted_url}, is_created: {is_created}")
    return JSONResponse({"short_id": shorted_url.short_id})


@router.get("/{short_id}")
async def redirect_short(short_id: str, db: AsyncSession = Depends(get_pg_session)):
    try:
        shorted_url = await ShortedUrlDAO.inc_visits_count(db, short_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Not found")

    return RedirectResponse(shorted_url.original_url)


@router.get("/stats/{short_id}", response_model=StatsResponse)
async def stats(short_id: str, db: AsyncSession = Depends(get_pg_session)):
    try:
        shorted_url = await ShortedUrlDAO.get_filtered(db, ShortedUrl.short_id == short_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Not found")

    return JSONResponse({
        "short_id": shorted_url.short_id,
        "url": shorted_url.original_url,
        "visits": shorted_url.visits
    })
