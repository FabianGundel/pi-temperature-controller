# PI Temperature Controller – Water Bath System

---

## Project Overview

This project is a self-developed **PI-based temperature control system** for a water bath, implemented using an Arduino UNO.

> First a PID-Controller was tryed to be implemented, but after some 
> development time and research the D-Part of the controller came out to be 
> unnecessary and was thrown out.

The goal is precise temperature regulation of a 1L water container using a self-calibrated NTC thermistor and a PWM-controlled heating element.

This project is being build to better understand practical control engineering, temperature measurement, PWM power control and sensor calibration. Instead of using a ready-made thermostat module, the entire control loop is being implemented using an Arduino UNO, a MOSFET-driven heating element and a self-calibrated NTC thermistor.

---

## Project Objectives

- Design and implementation of a closed-loop control system
- Development of a PI control algorithm
- Calibration of an NTC temperature sensor [NTC-Calibration](docs/calibration.md)
- Implementation of PWM-based power control

---

## Hardware

[Hardware](hardware/pi-temperature-controller-hardware.pdf)

---

## Circuit

[Main Circuit Diagram](docs/main.pdf)

[Images](images/)

> A 100nF decoupling capacitor was added between A0 and GND
> to filter high-frequency noise on the ADC input.

---

## PI-Controller

The System got calibrated on heating the water up to 35°C and holding the tempearture there consistently.

[Temperature Curve Image](images/PI-Curve.png)

[PI-Documentation](docs/pi.md)

---

## Code

[PI-Temperature-Regulation Code](src/main/main.ino)

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
- PI control algorithm

### 3. Power Stage
- MOSFET: IRLB8743
- PWM-controlled switching
- Heating element: 12V / 40W epoxy-sealed heater
- Power supply: 12V / 60W

### 4. Actuator
- Immersed heating element inside the water bath

---

## Current Status

✔ Hardware fully assembled 
✔ MOSFET successfully tested 
✔ NTC sensor calibrated 
✔ Temperature measurement functional 
✔ Control algorithm implemented
✔ PI parameter tuning finished

---

## Tools

> These tools were built with AI assistance and are provided
> as-is for development use. The core PI implementation
> in src/ was developed and understood independently.

The PI tuning process requires observing temperature curves over
several minutes. The Arduino Serial Plotter resets its time axis
on each reconnect and offers no export functionality.

- [Server](tools/host/localhost-pid-data.py): lightweight local server that receives and stores
  incoming temperature data
  
- [Uploader](tools/upload/serial-to-localhost.py): reads Serial output from the Arduino and forwards
  it to the server
  
- [Visualizer](tools/plotter/plotter.py): plots the live temperature curve with a
  time axis for better readability on slow thermal systems 

---

## License

MIT
