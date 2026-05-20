# Compile Reflection

Use this reference when fixing generated embedded code from compiler output.

## Triage Order

1. First real compiler error in the owning source file.
2. Type/signature mismatches caused by HAL, LL, ESP-IDF, or project-local APIs.
3. Missing include or feature macro.
4. Linker errors from duplicate symbols, wrong weak override, or missing object file.
5. Warnings that indicate runtime risk: implicit conversion, uninitialized value, packed struct alignment, ISR attribute mismatch.

## Repair Rules

- Match the codebase's existing peripheral API style.
- Preserve CubeMX `USER CODE BEGIN` and `USER CODE END` blocks.
- Prefer compile-time constants for pin/timer/channel choices.
- Avoid introducing dynamic allocation in low-level drivers unless already used locally.
- Add minimal tests or host-side checks when firmware cannot be flashed.

## Reflection Packet

When handing errors back to a generation step, include:

```text
target:
build command:
first error:
related warning:
source file:
suspected cause:
smallest repair:
```
