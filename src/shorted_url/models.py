from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.db.pg import PgModel


class ShortedUrl(PgModel):
    __tablename__ = "shorted_url"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False, unique=True)
    short_id = Column(String, nullable=False, unique=True)
    visits = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self):
        return str(self)

