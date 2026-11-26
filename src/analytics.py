"""Comparison calculations for canonical MarketPulse price rows."""


def index_by_date(prices):
    return {row["date"]: row for row in prices}


def align_series(instrument_prices, benchmark_prices):
    """Return the two series in chronological order on their shared dates."""
    instrument_by_date = index_by_date(instrument_prices)
    benchmark_by_date = index_by_date(benchmark_prices)
    common_dates = sorted(instrument_by_date.keys() & benchmark_by_date.keys())
    return (
        [instrument_by_date[date] for date in common_dates],
        [benchmark_by_date[date] for date in common_dates],
    )


def calculate_period_return(prices):
    """Return the percentage change across chronologically ordered rows."""
    first_close = prices[0]["close"]
    last_close = prices[-1]["close"]
    return (last_close / first_close - 1) * 100


def calculate_base_100(prices):
    """Rebase chronologically ordered closes to 100 on the first date."""
    first_close = prices[0]["close"]
    return [
        {"date": row["date"], "ticker": row["ticker"], "value": row["close"] / first_close * 100}
        for row in prices
    ]


def calculate_relative_performance(instrument_return, benchmark_return):
    """Return instrument outperformance in percentage points."""
    return instrument_return - benchmark_return
