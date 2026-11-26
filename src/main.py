from pathlib import Path
import json


from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)

from providers.yahoo_provider import YAHOO_SYMBOLS, fetch_yahoo_prices


DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def main():
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]
    instrument_ticker = instrument["ticker"]
    benchmark_ticker = benchmark["ticker"]
    try:
        instrument_prices = fetch_yahoo_prices(
            symbol=YAHOO_SYMBOLS[instrument_ticker],
            canonical_ticker=instrument_ticker,
        )
        benchmark_prices = fetch_yahoo_prices(
            symbol=YAHOO_SYMBOLS[benchmark_ticker],
            canonical_ticker=benchmark_ticker,
        )
    except ValueError as error:
        raise SystemExit(str(error)) from error

    aligned_instrument, aligned_benchmark = align_series(instrument_prices, benchmark_prices)
    if not aligned_instrument:
        raise SystemExit("Instrument and benchmark have no common observation dates.")

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative_performance = calculate_relative_performance(instrument_return, benchmark_return)
    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)

    print("=== MarketPulse ===")
    print()
    print("Provider")
    print("Yahoo Finance via yfinance")
    print()
    print("Market configuration")
    print(f"Period   : {LOOKBACK_LABEL}")
    print(f"Interval : {INTERVAL_LABEL}")
    print()
    print("Instrument")
    print(f"{instrument_ticker} - {instrument['name']}")
    print(f"Period return : {instrument_return:.2f}%")
    print()
    print("Benchmark")
    print(f"{benchmark_ticker} - {benchmark['name']}")
    print(f"Period return : {benchmark_return:.2f}%")
    print()
    print("Relative performance")
    print(f"{instrument_ticker} vs {benchmark_ticker} : {relative_performance:+.2f} percentage points")
    print()
    print("Base 100")
    print(f"{instrument_ticker:<6}: {instrument_base_100[0]['value']:.2f} -> {instrument_base_100[-1]['value']:.2f}")
    print(f"{benchmark_ticker:<6}: {benchmark_base_100[0]['value']:.2f} -> {benchmark_base_100[-1]['value']:.2f}")


if __name__ == "__main__":
    main()
