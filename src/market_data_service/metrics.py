from prometheus_client import Counter, Gauge

events_received = Counter(
    "market_data_events_received_total",
    "Total number of market data events received",
)

staleness_seconds = Gauge(
    "market_data_staleness_seconds",
    "Age of the most recently received market data",
)
