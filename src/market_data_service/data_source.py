import asyncio
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from typing import Protocol

from market_data_service.models import MarketDataEvent


class MarketDataSource(Protocol):
    async def stream(self) -> AsyncIterator[MarketDataEvent]: ...


class FakeMarketDataSource:
    def __init__(
        self,
        symbol: str,
        interval_seconds: float = 1.0,
    ) -> None:
        self.symbol = symbol
        self.interval_seconds = interval_seconds
        self.running = True

    async def stream(self) -> AsyncIterator[MarketDataEvent]:
        price = 100.0

        while self.running:
            yield MarketDataEvent(
                symbol=self.symbol,
                price=price,
                timestamp=datetime.now(UTC),
                source="fake",
            )

            price += 0.10

            await asyncio.sleep(self.interval_seconds)

    def stop(self) -> None:
        self.running = False
