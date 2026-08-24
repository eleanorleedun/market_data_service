from market_data_service.consumer import MarketDataConsumer
from market_data_service.staleness import StalenessDetector


class AppState:
    def __init__(
        self,
        consumer: MarketDataConsumer,
        staleness_detector: StalenessDetector,
    ) -> None:
        self.consumer = consumer
        self.staleness_detector = staleness_detector
