import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

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


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    state = create_state()

    consumer_task = asyncio.create_task(state.consumer.run())

    monitoring_task = asyncio.create_task(
        monitor_staleness(
            state.staleness_detector,
        )
    )

    app.state.market_data = state

    try:
        yield
    finally:
        consumer_task.cancel()
        monitoring_task.cancel()

        with suppress(asyncio.CancelledError):
            await consumer_task

        with suppress(asyncio.CancelledError):
            await monitoring_task


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
    )

    @app.get("/health/live")
    async def liveness() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health/ready")
    async def readiness() -> dict[str, str]:
        state: AppState = app.state.market_data

        if state.staleness_detector.is_stale:
            return {"status": "not_ready"}

        return {"status": "ready"}

    @app.get("/metrics")
    async def metrics() -> Response:
        return Response(
            content=generate_latest(),
            media_type=CONTENT_TYPE_LATEST,
        )

    return app
