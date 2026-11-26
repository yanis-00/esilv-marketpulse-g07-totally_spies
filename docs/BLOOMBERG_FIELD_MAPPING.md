# Bloomberg Field Mapping

## Access mode

**APPROVED_SAMPLE**

TD09 uses the repository's [Bloomberg teaching sample](../data/sample/bloomberg_reference_sample.json). The fixture records its mode as `approved_sample`. Live Bloomberg connectivity was not demonstrated. The lab cites `docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md` as the instructor reference. The mappings below were checked against the sample's schema note and the [expected canonical rows](../data/sample/bloomberg_reference_expected.json).

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
| --- | --- | --- |
| Instrument | `AAPL` | `AAPL US Equity` |
| Benchmark | `SP500` | `SPX Index` |

Both series contain 21 observations dated 2026-09-01 through 2026-09-30. The first observation records an AAPL close of 250 and an SP500 close of 6600.

## Field mapping

The source is a JSON object containing a `series` array. Each series has `role`, `canonical_ticker`, `provider_identifier`, and an `observations` array. The observation keys below are teaching wrapper keys, not live Bloomberg field mnemonics.

| MarketPulse field | Source field or mapping | Status / notes |
| --- | --- | --- |
| `date` | `observation_date` | Keep the `YYYY-MM-DD` string. |
| `ticker` | Parent series `canonical_ticker` | Preserve `AAPL` or `SP500`; use `provider_identifier` to identify the input series. |
| `open` | `open_value` | Convert to float. |
| `high` | `high_value` | Convert to float. |
| `low` | `low_value` | Convert to float. |
| `close` | `close_value` | Convert to float. |
| `volume` | `volume_value` | Convert to integer. The benchmark volume is explicitly zero in the sample. |

## TD10 handoff

- **Access mode** — `APPROVED_SAMPLE`.
- **Instrument identifier** — `AAPL US Equity`.
- **Benchmark identifier** — `SPX Index`.
- **Date representation** — ISO calendar date strings (`YYYY-MM-DD`).
- **Input structure** — One JSON object with two series, each containing its own observations.
- **Missing fields** — All six observation keys are present and non-null in both inspected series.
- **Normalization** — Build canonical rows with the parent series' canonical ticker. Preserve the sample's explicit zero benchmark volume. Pass the normalized rows to the existing alignment and analytics functions.
- **Expected canonical reference** — [bloomberg_reference_expected.json](../data/sample/bloomberg_reference_expected.json).
