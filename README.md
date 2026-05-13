# PID Temperature Controller – Water Bath System

> This project is currently work in progress.
> Source code and additional documentation will be uploaded progressively during development.

## Project Overview

This project is a self-developed **PID-based temperature control system** for a water bath, implemented using an Arduino UNO.

The goal is precise temperature regulation of a 1L water container using a self-calibrated NTC thermistor and a PWM-controlled heating element.

This projekt is being build to better understand practical control engineering, temperature measurement, PWM power control and sensor calibration. Instead of using a ready-made thermostat module, the entire control loop is being implemented using an Arduino UNO, a MOSFET-driven heating element and a self-calibrated NTC thermistor.

---

## Project Objectives

- Design and implementation of a closed-loop control system
- Development of a PID control algorithm
- Calibration of an NTC temperature sensor [NTC-Calibration](docs/calibration.md)
- Implementation of PWM-based power control

---

## Hardware

[Hardware](hardware/pid-temperature-controller-hardware.pdf)

---

## Circuit

[Main Circuit Diagram](docs/main.pdf)

---

## System Architecture

### 1. Temperature Measurement
- Waterproof 10kΩ NTC thermistor (25°C reference)
- 2660Ω reference resistor
- Temperature calculation using the Steinhart–Hart equation

### 2. Signal Processing
- Arduino UNO microcontroller
- Real-time temperature computation
- Error calculation (setpoint vs. measured value)
- PID control algorithm

### 3. Power Stage
- MOSFET: IRLB8743
- PWM-controlled switching
- Heating element: 12V / 40W epoxy-sealed heater
- Power supply: 12V / 60W

### 4. Actuator
- Immersed heating element inside the water bath

---

## System Characteristics

- Closed-loop feedback architecture
- Self-calibrated temperature sensor
- Power-efficient MOSFET switching stage
- Embedded real-time control
- Practical implementation of control engineering principles
- Consideration of thermal system dynamics

---

## Current Status

✔ Hardware fully assembled 
✔ MOSFET successfully tested 
✔ NTC sensor calibrated 
✔ Temperature measurement functional 
- Control algorithm implementation ongoing 
- PID parameter tuning ongoing 

---

### Licence

MIT
