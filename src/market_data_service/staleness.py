from datetime import UTC, datetime

from market_data_service.consumer import MarketDataConsumer
from market_data_service.metrics import staleness_seconds


class StalenessDetector:
    def __init__(
        self,
        consumer: MarketDataConsumer,
        stale_after_seconds: float,
    ) -> None:
        self.consumer = consumer
        self.stale_after_seconds = stale_after_seconds

    def data_age_seconds(self) -> float:
        if self.consumer.last_received_at is None:
            return float("inf")

        now = datetime.now(UTC)

        return (now - self.consumer.last_received_at).total_seconds()

    @property
    def is_stale(self) -> bool:
        return self.data_age_seconds() > self.stale_after_seconds

    def update_metrics(self) -> None:
        age = self.data_age_seconds()

        if age != float("inf"):
            staleness_seconds.set(age)
