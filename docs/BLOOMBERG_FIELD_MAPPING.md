# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

- Source: `data/sample/bloomberg_reference_sample.json`
- Expected canonical result: `data/sample/bloomberg_reference_expected.json`
- Live connectivity: not demonstrated
- The sample declares `is_live_bloomberg_output: false`. Its values are illustrative teaching values reused from `data/sample/prices.csv`, not certified Bloomberg historical observations.
- `docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md` was not available in the team repository when this document was written. The mapping below was checked against the expected canonical result.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

The canonical ticker is the one used by MarketPulse analytics. The Bloomberg identifier belongs to the provider boundary only.

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `observation_date` | ISO string `YYYY-MM-DD` in the inspected rows |
| ticker | application mapping | `AAPL` or `SP500`, taken from `canonical_ticker`, never from the Bloomberg identifier |
| open | `open_value` | Teaching wrapper key; numeric value |
| high | `high_value` | Teaching wrapper key; numeric value |
| low | `low_value` | Teaching wrapper key; numeric value |
| close | `close_value` | Teaching wrapper key; numeric value |
| volume | `volume_value` | Teaching wrapper key; integer value |

`observation_date`, `open_value`, `high_value`, `low_value`, `close_value` and `volume_value` are teaching wrapper keys. They are not Bloomberg field mnemonics, and no LIVE Bloomberg field name is claimed in this document.

## TD10 handoff

- Access mode: APPROVED_SAMPLE (live connectivity not demonstrated)
- Instrument identifier: AAPL US Equity (canonical ticker AAPL)
- Benchmark identifier: SPX Index (canonical ticker SP500)
- Date representation: string `YYYY-MM-DD`
- Input structure: a `series` list; each series has `role`, `canonical_ticker`, `provider_identifier` and an `observations` list
- Missing fields: none observed in the inspected observations
- Special normalization notes:
  - the benchmark series (`SPX Index`) has `volume_value: 0` in the inspected rows, so a volume of 0 is a valid value for an index and must not be treated as missing data;
  - some JSON numbers are integers (for example `low_value: 248`), so `open`, `high`, `low` and `close` must be converted to `float`, and `volume` to `int`;
  - the canonical ticker comes from `canonical_ticker`, so `SPX Index` must not appear in the canonical rows;
  - expected canonical reference: `data/sample/bloomberg_reference_expected.json`.