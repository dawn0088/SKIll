# Token Quota Application Narrative

## Project Summary

We have built an LLM-powered embedded hardware/software co-debugging system based on long-context reasoning, state-machine orchestration, and a multi-agent debug loop. The system targets STM32, ESP32, sensors, motor-control firmware, hardware schematics, datasheets, generated C code, compiler diagnostics, serial logs, SWD dumps, and PID response data.

The system has been deployed with a 15-person core hardware development team in an innovation base and robotics studio. It has reduced embedded hardware/software integration and bring-up cycles by approximately 65%.

## Core Pain Points

Embedded teams lose substantial engineering time aligning heterogeneous sources:

- Hardware schematics, PCB pin maps, datasheets, register tables, CubeMX/ESP-IDF configuration, and C source code.
- Pin multiplexing, boot strap behavior, voltage compatibility, bus timing, and microsecond-level control-loop constraints.
- PID tuning, sensor jitter, occasional bus deadlock, watchdog resets, and intermittent electrical/software coupling failures.

Traditional debugging depends heavily on manual oscilloscope inspection, serial-log review, and experience-driven trial-and-error. A single low-level driver or motor-control bug can consume days or weeks.

## Agent Matrix

1. **Hardware specification perception agent**: Extracts structured facts from schematics, pin diagrams, datasheets, and timing tables.
2. **Architecture reasoning and code generation agent**: Converts hardware constraints into firmware state machines, timing budgets, control equations, and C/C++ implementation.
3. **Automated compilation and virtual execution agent**: Runs cross-compilation, captures diagnostics, reflects on source-level causes, and repairs generated code.
4. **Closed-loop debug and fault diagnosis agent**: Consumes serial logs, SWD dumps, exception stacks, PID curves, and trace data to infer root causes and trigger the next iteration.

## Why Higher Token Quota Is Required

This workload is not a short prompt-response workflow. Each debugging loop can include:

- Hundreds of pages of datasheets and register tables.
- Multi-page schematics and board pin mappings.
- Generated and hand-written firmware modules.
- Compiler logs, AST-level repair context, linker diagnostics, and warnings.
- Runtime traces, PID curves, fault dumps, and prior iteration history.

The system needs long context to keep hardware constraints, generated code, compiler feedback, and runtime evidence aligned across iterations. Cutting context aggressively increases the risk of pin conflicts, timing mistakes, unsafe motor behavior, or repeated compile/debug loops.

## Current Usage

- Team size: 15 core embedded hardware/software developers.
- Daily token usage: approximately 3.8M to 4.5M tokens.
- Primary scenarios: STM32/ESP32 bring-up, motor PID tuning, sensor integration, bus fault diagnosis, firmware generation, compiler repair, and runtime fault analysis.
- Measured outcome: approximately 65% reduction in hardware/software co-debugging cycle time.

## Expected Benefit From Quota Increase

Higher quota enables stable daily operation for the deployed team:

- Preserve long-context debugging state across full firmware iterations.
- Support parallel agent workflows without throttling critical compile/debug loops.
- Reduce failed iterations caused by truncated datasheet or log context.
- Expand usage from pilot projects to broader robotics and embedded-control workloads.

## Repository Evidence

This repository provides a reusable Codex skill that encodes the deployed workflow:

- `embedded-debug-agent-matrix/SKILL.md`: core operating procedure.
- `embedded-debug-agent-matrix/references/`: detailed workflows for hardware ingestion, state machines, compile reflection, and closed-loop diagnosis.
- `embedded-debug-agent-matrix/scripts/pin_conflict_checker.py`: deterministic helper for normalized pin-map validation.
