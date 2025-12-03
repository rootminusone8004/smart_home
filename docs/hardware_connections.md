# Hardware Connections (Phase 0)

This document explains how each sensor/module is connected to the Raspberry Pi.

---

## 📌 Raspberry Pi Pin Reference
We use **BCM GPIO numbers** in code.

Example:
- GPIO4  → `board.D4`
- GPIO17 → `board.D17`

Refer to: https://pinout.xyz

---

🛠️ **Circuit Connections**

## DHT11 Wiring
- VCC → 5V
- GND → GND (Raspberry Pi)
- DATA → GPIO4

> **Recommended:** Add a 10kΩ pull-up resistor between DATA and VCC.

## Two Relay Wiring
- VCC → 5V
- GND → GND (Raspberry Pi)
- IN1 → GPIO17
- IN2 → GPIO27

## LCD (16x2) Wiring (I2C version)
- VCC → 5V
- GND → GND (Raspberry Pi)
- SDA → SDA
- SCL → SCL

## Photo resistor
- VCC → 5V
- GND → GND

## Photo resistor
- VCC → 5V
- GND → GND
- DO → GPIO22
