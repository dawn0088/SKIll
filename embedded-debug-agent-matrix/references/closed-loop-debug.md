# Closed-Loop Debug

Use this reference when analyzing serial logs, dumps, traces, PID curves, or intermittent hardware faults.

## Diagnosis Flow

1. Classify the symptom: reset, bus lock, control oscillation, sensor noise, missing interrupt, thermal/current fault.
2. Align runtime timestamps with firmware states.
3. Compare observed timing against datasheet and configured timer/clock values.
4. Separate physical causes from software causes with a next-measurement plan.
5. Propose the smallest code or configuration change and the measurement that should improve.

## Common Patterns

- PID oscillation: sample period mismatch, derivative noise, output saturation without anti-windup, encoder quantization.
- I2C lock: missing pull-ups, bus held low after brownout, no timeout, recovery clock pulses missing.
- UART packet loss: ISR overwork, ring buffer overflow, baud mismatch, DMA idle-line handling bug.
- ESP32 boot failure: strapping pin pulled to the wrong level by attached peripheral.
- STM32 peripheral silent: alternate function mismatch, clock gate missing, DMA channel collision, NVIC priority issue.

## Output Shape

```text
observed symptom:
evidence:
most likely cause:
confidence:
next measurement:
proposed fix:
rollback/safety note:
```
