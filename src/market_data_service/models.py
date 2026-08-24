from datetime import datetime

from pydantic import BaseModel, Field


class MarketDataEvent(BaseModel):
    symbol: str = Field(min_length=1)
    price: float = Field(gt=0)
    timestamp: datetime
    source: str = Field(min_length=1)
