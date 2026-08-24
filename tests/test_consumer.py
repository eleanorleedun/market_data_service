import asyncio
from datetime import UTC, datetime

import pytest

from market_data_service.consumer import MarketDataConsumer
from market_data_service.models import MarketDataEvent


class FakeTestSource:
    async def stream(self):
        yield MarketDataEvent(
            symbol="AAPL",
            price=100.0,
            timestamp=datetime.now(UTC),
            source="test",
        )

        await asyncio.sleep(10)


@pytest.mark.asyncio
async def test_consumer_stores_latest_event():
    source = FakeTestSource()
    consumer = MarketDataConsumer(source)

    task = asyncio.create_task(consumer.run())

    await asyncio.sleep(0)

    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    assert consumer.latest_event is not None
    assert consumer.latest_event.symbol == "AAPL"
    assert consumer.latest_event.price == 100.0


def test_process_event_updates_state():
    consumer = MarketDataConsumer(FakeTestSource())

    event = MarketDataEvent(
        symbol="AAPL",
        price=150.0,
        timestamp=datetime.now(UTC),
        source="test",
    )

    before = datetime.now(UTC)

    consumer.process_event(event)

    after = datetime.now(UTC)

    assert consumer.latest_event == event
    assert consumer.events_received == 1
    assert consumer.last_received_at is not None
    assert before <= consumer.last_received_at <= after
