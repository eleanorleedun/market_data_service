from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from market_data_service.models import MarketDataEvent


def test_valid_market_data_event():
    timestamp = datetime.now(UTC)

    event = MarketDataEvent(
        symbol="AAPL",
        price=231.45,
        timestamp=timestamp,
        source="yfinance",
    )

    assert event.symbol == "AAPL"
    assert event.price == 231.45
    assert event.timestamp == timestamp
    assert event.source == "yfinance"


def test_price_must_be_positive():
    with pytest.raises(ValidationError):
        MarketDataEvent(
            symbol="AAPL",
            price=-1,
            timestamp=datetime.now(UTC),
            source="yfinance",
        )


def test_symbol_cannot_be_empty():
    with pytest.raises(ValidationError):
        MarketDataEvent(
            symbol="",
            price=231.45,
            timestamp=datetime.now(UTC),
            source="yfinance",
        )


def test_source_cannot_be_empty():
    with pytest.raises(ValidationError):
        MarketDataEvent(
            symbol="AAPL",
            price=231.45,
            timestamp=datetime.now(UTC),
            source="",
        )
