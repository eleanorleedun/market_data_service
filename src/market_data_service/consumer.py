from datetime import UTC, datetime

from market_data_service.data_source import MarketDataSource
from market_data_service.metrics import events_received
from market_data_service.models import MarketDataEvent


class MarketDataConsumer:
    def __init__(self, source: MarketDataSource) -> None:
        self.source = source
        self.latest_event: MarketDataEvent | None = None
        self.last_received_at: datetime | None = None
        self.events_received = 0

    def process_event(self, event: MarketDataEvent) -> None:
        self.latest_event = event
        self.last_received_at = datetime.now(UTC)
        self.events_received += 1
        events_received.inc()

    async def run(self) -> None:
        async for event in self.source.stream():
            self.process_event(event)
