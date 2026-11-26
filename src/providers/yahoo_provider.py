"""Fetch Yahoo Finance history as canonical MarketPulse rows."""

import yfinance as yf


YAHOO_SYMBOLS = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",
}


def fetch_yahoo_prices(symbol, canonical_ticker, period="1mo", interval="1d"):
    """Return historical OHLCV rows with the MarketPulse ticker."""
    history = yf.Ticker(symbol).history(
        period=period,
        interval=interval,
        auto_adjust=False,
    )
    if history.empty:
        raise ValueError(f"No Yahoo Finance data returned for {symbol}")

    return [
        {
            "date": timestamp.strftime("%Y-%m-%d"),
            "ticker": canonical_ticker,
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]),
        }
        for timestamp, row in history.iterrows()
    ]
