import json
from pathlib import Path

ACCESS_MODE = "APPROVED_SAMPLE"

SAMPLE_PATH = Path("data/sample/bloomberg_reference_sample.json")

# Bloomberg identifiers stay at the provider boundary.
BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}


def fetch_raw_bloomberg_history(identifier):
    """Return the approved raw series for a Bloomberg identifier (APPROVED_SAMPLE mode)."""
    with open(SAMPLE_PATH, encoding="utf-8") as file:
        sample = json.load(file)

    for series in sample["series"]:
        if series["provider_identifier"] == identifier:
            return series

    raise ValueError(f"No approved sample series for {identifier}")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    """Convert approved Bloomberg-stage input into canonical MarketPulse rows."""
    rows = []

    for observation in raw_data["observations"]:
        rows.append({
            "date": observation["observation_date"],
            "ticker": canonical_ticker,
            "open": float(observation["open_value"]),
            "high": float(observation["high_value"]),
            "low": float(observation["low_value"]),
            "close": float(observation["close_value"]),
            "volume": int(observation["volume_value"]),
        })

    return rows


def fetch_bloomberg_prices(canonical_ticker):
    """Return canonical rows for a canonical ticker (AAPL or SP500)."""
    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]
    raw_data = fetch_raw_bloomberg_history(identifier)

    return normalize_bloomberg_history(raw_data, canonical_ticker)