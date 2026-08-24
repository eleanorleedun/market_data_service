from market_data_service.config import Settings


def test_default_settings():
    settings = Settings()

    assert settings.market_symbol == "AAPL"
    assert settings.stale_after_seconds == 10.0
    assert settings.port == 8000
