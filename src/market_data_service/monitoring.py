import asyncio

from market_data_service.staleness import StalenessDetector


async def monitor_staleness(
    detector: StalenessDetector,
    interval_seconds: float = 1.0,
) -> None:
    while True:
        detector.update_metrics()
        await asyncio.sleep(interval_seconds)
