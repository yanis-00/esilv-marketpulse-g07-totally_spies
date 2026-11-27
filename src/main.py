from pathlib import Path
import csv
import json

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from providers.bloomberg_provider import (
    ACCESS_MODE as BLOOMBERG_ACCESS_MODE,
    fetch_bloomberg_prices,
)
from providers.yahoo_provider import fetch_yahoo_prices

# MarketPulse - main entry point
DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"

# Canonical ticker -> Yahoo-specific symbol (provider boundary only)
YAHOO_SYMBOLS = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",
}


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def normalize_price_row(row):
    return {
        "date": row["date"],
        "ticker": row["ticker"],
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": int(row["volume"]),
    }


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def fetch_prices(provider, canonical_ticker):
    """Return canonical rows for one canonical ticker from the chosen provider."""
    if provider == "bloomberg":
        return fetch_bloomberg_prices(canonical_ticker)

    if provider == "yahoo":
        return fetch_yahoo_prices(
            symbol=YAHOO_SYMBOLS[canonical_ticker],
            canonical_ticker=canonical_ticker,
            period="1mo",
            interval="1d",
        )

    raise ValueError(f"Unsupported provider: {provider}")


def build_market_snapshot(provider="bloomberg"):
    """Build the shared application result used by the terminal presentation."""
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = fetch_prices(provider, instrument["ticker"])
    benchmark_prices = fetch_prices(provider, benchmark["ticker"])

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)

    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    if provider == "bloomberg":
        provider_label = "Bloomberg stage"
        access_mode = BLOOMBERG_ACCESS_MODE
    else:
        provider_label = "Yahoo Finance via yfinance"
        access_mode = "LIVE"

    return {
        "provider": provider_label,
        "access_mode": access_mode,
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": instrument,
        "benchmark": benchmark,
        "common_dates": len(aligned_instrument),
        "first_date": aligned_instrument[0]["date"],
        "last_date": aligned_instrument[-1]["date"],
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": relative_performance,
        "instrument_base_100": calculate_base_100(aligned_instrument),
        "benchmark_base_100": calculate_base_100(aligned_benchmark),
    }


def main():
    snapshot = build_market_snapshot()

    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    instrument_base_100 = snapshot["instrument_base_100"]
    benchmark_base_100 = snapshot["benchmark_base_100"]

    print("=== MarketPulse ===")
    print()
    print("Provider")
    print(snapshot["provider"])
    print()
    print("Access mode")
    print(snapshot["access_mode"])
    print()
    print("Market configuration")
    print(f"Instrument : {instrument['ticker']} - {instrument['name']}")
    print(f"Benchmark  : {benchmark['name']}")
    print(f"Period     : {snapshot['lookback']}")
    print(f"Interval   : {snapshot['interval']}")
    print()
    print(f"Common dates : {snapshot['common_dates']}")
    print(f"First date   : {snapshot['first_date']}")
    print(f"Last date    : {snapshot['last_date']}")
    print()
    print(f"Instrument return : {snapshot['instrument_return']:.2f}%")
    print(f"Benchmark return  : {snapshot['benchmark_return']:.2f}%")
    print()
    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{snapshot['relative_performance']:+.2f} percentage points"
    )
    print()
    print("Base 100")
    print(
        f"{instrument['ticker']:<6}: "
        f"{instrument_base_100[0]['value']:.2f} -> "
        f"{instrument_base_100[-1]['value']:.2f}"
    )
    print(
        f"{benchmark['ticker']:<6}: "
        f"{benchmark_base_100[0]['value']:.2f} -> "
        f"{benchmark_base_100[-1]['value']:.2f}"
    )


if __name__ == "__main__":
    main()