#!/usr/bin/env python3
"""Check normalized embedded pin maps for common bring-up risks."""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path


SPECIAL_PINS = {
    "BOOT0",
    "NRST",
    "SWDIO",
    "SWCLK",
    "JTMS",
    "JTCK",
    "OSC_IN",
    "OSC_OUT",
    "GPIO0",
    "GPIO2",
    "GPIO12",
    "GPIO15",
    "EN",
}


REQUIRED_COLUMNS = {"signal", "mcu_pin", "peripheral", "direction", "voltage", "timing", "source"}


def normalize(value: str) -> str:
    return " ".join((value or "").strip().upper().split())


def check_pinmap(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - fieldnames
        if missing:
            return [f"ERROR missing columns: {', '.join(sorted(missing))}"]

        rows = list(reader)

    issues: list[str] = []
    by_pin: dict[str, list[dict[str, str]]] = defaultdict(list)

    for index, row in enumerate(rows, start=2):
        pin = normalize(row["mcu_pin"])
        signal = row["signal"].strip()
        voltage = normalize(row["voltage"])
        source = row["source"].strip()
        peripheral = normalize(row["peripheral"])

        if not pin:
            issues.append(f"ERROR line {index}: signal {signal!r} has no MCU pin")
            continue

        by_pin[pin].append(row)

        if pin in SPECIAL_PINS:
            issues.append(f"WARN line {index}: {signal} uses special/debug/boot pin {pin}")
        if not source:
            issues.append(f"WARN line {index}: {signal} on {pin} has no source evidence")
        if "5V" in voltage or "5 V" in voltage:
            issues.append(f"WARN line {index}: {signal} on {pin} references 5 V; verify tolerance or level shifting")
        if peripheral == "I2C" and "OPEN" not in normalize(row["direction"]):
            issues.append(f"WARN line {index}: {signal} is I2C; verify open-drain mode and pull-ups")

    for pin, pin_rows in sorted(by_pin.items()):
        if len(pin_rows) <= 1:
            continue
        signals = ", ".join(row["signal"].strip() for row in pin_rows)
        issues.append(f"ERROR duplicate pin {pin}: {signals}")

    return issues


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: pin_conflict_checker.py pinmap.csv", file=sys.stderr)
        return 2

    path = Path(argv[1])
    issues = check_pinmap(path)
    if not issues:
        print("OK pin map passed basic conflict checks")
        return 0

    for issue in issues:
        print(issue)
    return 1 if any(issue.startswith("ERROR") for issue in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
