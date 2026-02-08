## Context

The app currently lacks a data size converter despite supporting other common unit types. This change adds a new converter for bit/byte and decimal/binary prefixed units, with UI exposure and tests, following the existing converter plugin pattern.

## Goals / Non-Goals

**Goals:**
- Introduce a dedicated data unit converter that supports bit, byte, and standard decimal/binary prefixes.
- Ensure the converter is registered and selectable in the UI.
- Provide test coverage for common conversions and edge cases.

**Non-Goals:**
- Adding specialized data rate conversions (e.g., Mbps) or time-based units.
- Supporting uncommon or legacy units beyond standard bit/byte prefixes.

## Decisions

- Implement a new `Converter` subclass under `src/converters/` to align with the plugin architecture and keep conversion logic isolated per unit type.
- Represent units via a normalized base (bits) and map each unit to a multiplier, enabling straightforward conversion through base normalization.
- Use 1024-based multipliers for KB/MB/GB/TB to align with traditional expectations; keep KiB/MiB/GiB/TiB for explicit binary labeling.

## Risks / Trade-offs

- Unit ambiguity (KB vs KiB) could confuse users → Explicitly list both labels in the UI and document that both follow 1024-based sizing.
- Large magnitude conversions may risk floating point precision → Use float math consistently as in existing converters and validate with tests on boundary values.
