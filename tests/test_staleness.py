from datetime import UTC, datetime, timedelta

from market_data_service.consumer import MarketDataConsumer
from market_data_service.data_source import FakeMarketDataSource
from market_data_service.staleness import StalenessDetector


def create_consumer() -> MarketDataConsumer:
    source = FakeMarketDataSource("AAPL")
    return MarketDataConsumer(source)


def test_no_data_is_stale():
    consumer = create_consumer()

    detector = StalenessDetector(
        consumer=consumer,
        stale_after_seconds=10,
    )

    assert detector.is_stale is True


def test_recent_data_is_not_stale():
    consumer = create_consumer()

    consumer.last_received_at = datetime.now(UTC)

    detector = StalenessDetector(
        consumer=consumer,
        stale_after_seconds=10,
    )

    assert detector.is_stale is False


def test_old_data_is_stale():
    consumer = create_consumer()

    consumer.last_received_at = datetime.now(UTC) - timedelta(seconds=20)

    detector = StalenessDetector(
        consumer=consumer,
        stale_after_seconds=10,
    )

    assert detector.is_stale is True


def test_data_age():
    consumer = create_consumer()

    consumer.last_received_at = datetime.now(UTC) - timedelta(seconds=5)

    detector = StalenessDetector(
        consumer=consumer,
        stale_after_seconds=10,
    )

    age = detector.data_age_seconds()

    assert 4.0 <= age <= 6.0
