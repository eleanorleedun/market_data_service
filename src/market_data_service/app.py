from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from market_data_service.config import get_settings
from market_data_service.state import AppState


def create_app(state: AppState) -> FastAPI:
    settings = get_settings()

    app = FastAPI(title=settings.app_name)

    @app.get("/health/live")
    async def liveness() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health/ready")
    async def readiness() -> dict[str, str]:
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
