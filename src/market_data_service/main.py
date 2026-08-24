import asyncio
from contextlib import suppress

import uvicorn

from market_data_service.app import create_app
from market_data_service.config import get_settings
from market_data_service.consumer import MarketDataConsumer
from market_data_service.data_source import FakeMarketDataSource
from market_data_service.monitoring import monitor_staleness
from market_data_service.staleness import StalenessDetector
from market_data_service.state import AppState


def create_state() -> AppState:
    settings = get_settings()

    source = FakeMarketDataSource(
        symbol=settings.market_symbol,
    )

    consumer = MarketDataConsumer(source)

    staleness_detector = StalenessDetector(
        consumer=consumer,
        stale_after_seconds=settings.stale_after_seconds,
    )

    return AppState(
        consumer=consumer,
        staleness_detector=staleness_detector,
    )


async def run() -> None:
    settings = get_settings()
    state = create_state()

    app = create_app(state)

    consumer_task = asyncio.create_task(state.consumer.run())

    monitoring_task = asyncio.create_task(
        monitor_staleness(
            state.staleness_detector,
        )
    )

    server_config = uvicorn.Config(
        app,
        host=settings.host,
        port=settings.port,
    )

    server = uvicorn.Server(server_config)

    try:
        await server.serve()
    finally:
        consumer_task.cancel()
        monitoring_task.cancel()

        with suppress(asyncio.CancelledError):
            await consumer_task

        with suppress(asyncio.CancelledError):
            await monitoring_task


def main() -> None:
    asyncio.run(run())

