import pytest

from market_data_service.data_source import FakeMarketDataSource


@pytest.mark.asyncio
async def test_fake_data_source_produces_events():
    source = FakeMarketDataSource(
        symbol="AAPL",
        interval_seconds=0,
    )

    stream = source.stream()

    event = await anext(stream)

    assert event.symbol == "AAPL"
    assert event.price == 100.0
    assert event.source == "fake"


@pytest.mark.asyncio
async def test_fake_data_source_produces_increasing_prices():
    source = FakeMarketDataSource(
        symbol="AAPL",
        interval_seconds=0,
    )

    stream = source.stream()

    first = await anext(stream)
    second = await anext(stream)

    assert second.price > first.price


@pytest.mark.asyncio
async def test_fake_data_source_can_stop():
    source = FakeMarketDataSource(
        symbol="AAPL",
        interval_seconds=0,
    )

    stream = source.stream()

    first = await anext(stream)

    assert first.symbol == "AAPL"

    source.stop()

    with pytest.raises(StopAsyncIteration):
        await anext(stream)
