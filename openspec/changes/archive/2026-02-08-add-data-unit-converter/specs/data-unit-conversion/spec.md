## ADDED Requirements

### Requirement: Support data unit conversion
The system SHALL convert values between common data size units including bit, byte, and decimal/binary prefixed units.

#### Scenario: Convert between bit and byte
- **WHEN** a user converts a value from bit to byte or byte to bit
- **THEN** the system returns the mathematically correct value based on 8 bits per byte

#### Scenario: Convert between KB/MB/GB/TB units
- **WHEN** a user converts between KB, MB, GB, and TB
- **THEN** the system uses base-2 multipliers (1 KB = 1024 bytes)

#### Scenario: Convert between KiB/MiB/GiB/TiB units
- **WHEN** a user converts between KiB, MiB, GiB, and TiB
- **THEN** the system uses base-2 multipliers (1 KiB = 1024 bytes)

#### Scenario: Convert across KB and KiB units
- **WHEN** a user converts between KB and KiB (e.g., KB to KiB)
- **THEN** the system returns equal values based on 1024-based sizing

#### Scenario: Preserve value on same-unit conversion
- **WHEN** a user converts a value from a unit to the same unit
- **THEN** the system returns the original value unchanged
