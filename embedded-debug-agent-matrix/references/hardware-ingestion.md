# Hardware Ingestion

Use this reference when the task involves schematics, datasheets, pin maps, or board-level constraints.

## Extraction Checklist

- Identify MCU family, package, clock sources, power rails, reset circuit, debug header, boot straps.
- Extract each peripheral connection as `signal, mcu_pin, peripheral, direction, voltage, timing, source`.
- Preserve source anchors: schematic page, datasheet table, CubeMX section, or board silkscreen note.
- Flag assumptions explicitly when the source is a screenshot, partial PDF, or generated config without schematic confirmation.

## Risk Rules

- Treat `BOOT0`, `EN`, `GPIO0`, `GPIO2`, `GPIO12`, `GPIO15`, `NRST`, `SWDIO`, `SWCLK`, `OSC_IN`, and `OSC_OUT` as special-use pins until proven safe for the exact MCU/module.
- Treat I2C as open-drain with pull-up validation.
- Treat motor PWM, encoder capture, and step/dir signals as timing-critical.
- Treat ADC readings near motors, relays, or switching regulators as noise-sensitive.
- Do not mix 5 V signals into non-5 V tolerant pins without a level-shifting or resistor-divider note.

## Output Shape

Prefer compact tables:

```text
signal | mcu_pin | peripheral | direction | voltage | timing | source | risk
```

Add a short "Blocking Unknowns" list when code generation would be unsafe.
