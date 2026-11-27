import json
from pathlib import Path


from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)

from providers.bloomberg_provider import (
    ACCESS_MODE,
    load_bloomberg_sample,
    normalize_bloomberg_history,
)


DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "sample"

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def build_market_snapshot():
    """Build the shared application result for the terminal and dashboard."""
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    sample = load_bloomberg_sample()
    instrument_prices = normalize_bloomberg_history(sample, instrument["ticker"])
    benchmark_prices = normalize_bloomberg_history(sample, benchmark["ticker"])
    aligned_instrument, aligned_benchmark = align_series(instrument_prices, benchmark_prices)
    if not aligned_instrument:
        raise ValueError("Instrument and benchmark have no common observation dates.")

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    return {
        "provider": "Bloomberg stage",
        "access_mode": ACCESS_MODE,
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": calculate_relative_performance(
            instrument_return, benchmark_return
        ),
        "instrument_base_100": calculate_base_100(aligned_instrument),
        "benchmark_base_100": calculate_base_100(aligned_benchmark),
    }


def main():
    try:
        snapshot = build_market_snapshot()
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error

    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    instrument_ticker = instrument["ticker"]
    benchmark_ticker = benchmark["ticker"]
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
    print(f"Period   : {snapshot['lookback']}")
    print(f"Interval : {snapshot['interval']}")
    print()
    print("Instrument")
    print(f"{instrument_ticker} - {instrument['name']}")
    print(f"Period return : {snapshot['instrument_return']:.2f}%")
    print()
    print("Benchmark")
    print(f"{benchmark_ticker} - {benchmark['name']}")
    print(f"Period return : {snapshot['benchmark_return']:.2f}%")
    print()
    print("Relative performance")
    print(f"{instrument_ticker} vs {benchmark_ticker} : {snapshot['relative_performance']:+.2f} percentage points")
    print()
    print("Common observations")
    print(f"{len(instrument_base_100)} ({instrument_base_100[0]['date']} to {instrument_base_100[-1]['date']})")
    print()
    print("Base 100")
    print(f"{instrument_ticker:<6}: {instrument_base_100[0]['value']:.2f} -> {instrument_base_100[-1]['value']:.2f}")
    print(f"{benchmark_ticker:<6}: {benchmark_base_100[0]['value']:.2f} -> {benchmark_base_100[-1]['value']:.2f}")


if __name__ == "__main__":
    main()
