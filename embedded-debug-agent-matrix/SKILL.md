---
name: embedded-debug-agent-matrix
description: Embedded hardware/software co-debugging for STM32, ESP32, sensors, motor control, bus protocols, schematics, datasheets, CubeMX/ESP-IDF projects, C drivers, compiler logs, serial/SWD traces, PID curves, and automated long-context fault diagnosis. Use when Codex needs to extract hardware constraints, reason about pins/timing/registers, generate or repair embedded C/C++ code, run build-log reflection, or propose closed-loop debugging iterations.
---

# Embedded Debug Agent Matrix

## Operating Model

Use this skill as a state-machine-driven workflow for embedded bring-up and automated co-debugging. Treat the job as four cooperating agents:

1. **Hardware specification perception**: Convert schematics, datasheets, pin maps, CubeMX files, ESP-IDF config, BOM notes, and board photos into structured constraints.
2. **Architecture reasoning and code generation**: Derive firmware architecture, timing budgets, peripheral setup, control equations, and C/C++ changes from the constraints.
3. **Automated build and virtual execution**: Compile, capture errors/warnings, map diagnostics to source/AST-level causes, and iterate until the build is clean.
4. **Closed-loop debug and fault diagnosis**: Analyze serial logs, SWD dumps, bus traces, PID response curves, and intermittent failures; propose code, configuration, or hardware checks.

Keep final answers concise. Do not expose hidden chain-of-thought; provide the resulting assumptions, state transitions, equations, constraints, and decisions that matter for engineering review.

## Workflow

### 1. Build the Evidence Packet

Collect only the artifacts needed for the current stage:

- Hardware: schematic PDF pages, datasheet sections, pin tables, peripheral alternate-function tables, power tree, clock tree, connector mapping.
- Firmware: `*.ioc`, `sdkconfig`, `CMakeLists.txt`, linker script, startup file, HAL/LL/ESP-IDF driver files, interrupt handlers, FreeRTOS tasks.
- Runtime: compiler output, serial logs, SWD/JTAG dumps, logic-analyzer captures, PID setpoint/feedback/output CSV, reset reason, watchdog traces.

If datasheet or schematic context is missing, state the assumption and mark it as a validation item instead of inventing a pin, register, or timing number.

### 2. Normalize Hardware Constraints

Represent hardware facts in a small table or JSON-like block:

```text
signal | mcu_pin | peripheral | direction | voltage | timing | conflict_risk | source
```

Check these before code generation:

- Alternate-function conflicts, boot strap pins, SWD/JTAG pins, oscillator pins, ADC-only pins, input-only pins.
- Pull-up/pull-down requirements, open-drain buses, 5 V tolerance, level shifting, motor driver enable/fault pins.
- Clock source and timer resolution needed for PWM, encoder capture, UART/SPI/I2C baud, control-loop tick.
- Datasheet min/max timing, reset sequencing, bus timeout, chip-select hold time, sensor conversion latency.

For detailed extraction guidance, read `references/hardware-ingestion.md`.

### 3. Plan the Firmware State Machine

Before editing code, define the runtime states and transitions:

```text
BOOT -> HW_PROBE -> CONFIGURE_PERIPHERALS -> RUN_CONTROL_LOOP -> FAULT_RECOVERY -> SAFE_STOP
```

For PID/motion work, compute and show the engineering results:

- Mechanical ratio, pulses per revolution, counter overflow interval.
- Sampling period, discrete control law, anti-windup behavior, output saturation.
- Safety thresholds, fault latch/reset policy, watchdog timing.

For templates and examples, read `references/state-machine-patterns.md`.

### 4. Generate or Modify Firmware

Prefer the project's existing HAL, LL, ESP-IDF, FreeRTOS, or bare-metal style. Keep edits scoped:

- Put pin/peripheral constants in the existing board config layer.
- Keep interrupt handlers short; move work into queues, flags, or control-loop tasks.
- Handle timeouts and error returns for every blocking bus operation.
- Preserve user code blocks in CubeMX-generated files.
- Avoid touching unrelated clock, linker, startup, or scheduler configuration unless the evidence packet requires it.

### 5. Compile and Reflect

Run the local build command when available. On failure:

1. Capture the first real error plus related warnings.
2. Map the diagnostic to the owning module and generated change.
3. Repair the smallest source region that explains the failure.
4. Rebuild until clean or until a missing dependency/toolchain blocks progress.

For compiler-log triage patterns, read `references/compile-reflection.md`.

### 6. Close the Hardware Loop

For runtime faults, classify the symptom before proposing fixes:

- **Electrical**: brownout, level mismatch, missing pull-up, floating input, motor noise, ground bounce.
- **Timing**: bus setup/hold violation, ISR jitter, timer overflow, PID sample mismatch, blocking call in control path.
- **Software**: race condition, buffer overrun, wrong register mask, unhandled error, priority inversion.
- **Configuration**: wrong alternate function, DMA channel collision, clock mismatch, boot pin conflict.

Use evidence from logs or traces. When evidence is weak, propose the next measurement, not a confident root cause. For diagnosis flow, read `references/closed-loop-debug.md`.

## Reusable Tools

- `scripts/pin_conflict_checker.py`: Validate a normalized pin map CSV for duplicate MCU pin usage, boot/debug pin risks, voltage mismatch notes, and missing source evidence.

Expected CSV columns:

```text
signal,mcu_pin,peripheral,direction,voltage,timing,source
```

Run:

```bash
python scripts/pin_conflict_checker.py pinmap.csv
```
