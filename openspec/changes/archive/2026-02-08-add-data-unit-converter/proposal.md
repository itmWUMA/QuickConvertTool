## Why

Users need to convert common data size units (bit, byte, KB, MB, GB, etc.) but the app lacks a dedicated converter for these units. Adding this capability closes a notable gap in the conversion set and supports a frequent real-world use case.

## What Changes

- Add a new data unit converter that supports bit/byte and decimal/binary prefixes (KB/MB/GB/TB, KiB/MiB/GiB/TiB) in the conversion list.
- Expose the new converter in the UI alongside existing converters.
- Add tests covering standard conversions and edge cases for data units.

## Capabilities

### New Capabilities
- `data-unit-conversion`: Convert between common data size units including bit, byte, and decimal/binary prefixed units.

### Modified Capabilities

## Impact

- New converter implementation under `src/converters/` and registration in `src/main.py`.
- UI updates to include the data unit converter in selection.
- New test suite in `tests/` for data unit conversions.
