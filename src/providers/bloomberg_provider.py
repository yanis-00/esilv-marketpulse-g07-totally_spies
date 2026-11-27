"""Normalize the approved Bloomberg teaching fixture to MarketPulse rows."""

import json
from pathlib import Path


ACCESS_MODE = "APPROVED_SAMPLE"
BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}
SAMPLE_PATH = (
    Path(__file__).resolve().parents[2]
    / "data" / "sample" / "bloomberg_reference_sample.json"
)


def load_bloomberg_sample():
    """Read the approved Bloomberg-stage input."""
    with SAMPLE_PATH.open(encoding="utf-8") as file:
        sample = json.load(file)
    if sample["access_mode"].upper() != ACCESS_MODE:
        raise ValueError("Expected the approved Bloomberg teaching sample.")
    return sample


def normalize_bloomberg_history(raw_data, canonical_ticker):
    """Apply the TD09 mapping to the selected series' observations."""
    identifier = BLOOMBERG_IDENTIFIERS.get(canonical_ticker)
    if identifier is None:
        raise ValueError(f"Unsupported Bloomberg ticker: {canonical_ticker}")

    for series in raw_data["series"]:
        if series["provider_identifier"] == identifier:
            break
    else:
        raise ValueError(f"No Bloomberg sample series for {identifier}")

    if series["canonical_ticker"] != canonical_ticker:
        raise ValueError(f"Unexpected canonical ticker for {identifier}")

    return [
        {
            "date": observation["observation_date"],
            "ticker": series["canonical_ticker"],
            "open": float(observation["open_value"]),
            "high": float(observation["high_value"]),
            "low": float(observation["low_value"]),
            "close": float(observation["close_value"]),
            "volume": int(observation["volume_value"]),
        }
        for observation in series["observations"]
    ]
