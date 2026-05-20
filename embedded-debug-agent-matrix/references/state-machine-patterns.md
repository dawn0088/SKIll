# State Machine Patterns

Use this reference when designing firmware structure, PID loops, motor control, or fault recovery.

## Bring-Up State Machine

```text
BOOT
  -> CLOCK_READY
  -> GPIO_SAFE_DEFAULTS
  -> BUS_PROBE
  -> PERIPHERAL_CONFIGURED
  -> RUN
  -> FAULT_LATCHED
  -> SAFE_STOP
```

## Control Loop Derivation

For motion/PID work, derive:

```text
counts_per_output_rev = encoder_ppr * decode_factor * gear_ratio
overflow_seconds = timer_max_count / max_counts_per_second
Ts = control_loop_period_seconds
e[k] = setpoint[k] - feedback[k]
u[k] = clamp(Kp*e[k] + Ki*Ts*sum(e) + Kd*(e[k]-e[k-1])/Ts)
```

Check:

- `Ts` is stable and measured from a hardware timer or RTOS tick with bounded jitter.
- Integral term has anti-windup when output saturates.
- Encoder counter cannot overflow silently between samples.
- Fault state disables PWM or driver enable before logging lengthy diagnostics.

## Interrupt Boundaries

- ISR: timestamp, clear flag, copy sample, increment counter, notify task.
- Task/main loop: parse packets, run PID, log, retry buses, allocate memory.
- Never do blocking I2C/SPI/UART transactions in high-rate control ISRs.
