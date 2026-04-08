from pydantic import BaseModel, HttpUrl


class ShortenRequest(BaseModel):
    url: HttpUrl


class ShortenResponse(BaseModel):
    short_id: str


class StatsResponse(BaseModel):
    short_id: str
    url: HttpUrl
    visits: int
