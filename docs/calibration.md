# NTC Thermistor Calibration

Calibration of a NTC thermistor using the Steinhart-Hart equation for the water bath PID controller.

## Components

- NTC Thermistor: 10kΩ @ 25°C
- Reference resistor: 2660Ω
- Arduino Uno
- Reference thermometer

## Circuit

[Calibration Circuit Diagram](../docs/calibration.pdf)
 
## Code

[Calibration Code](../src/calibration/calibration.ino)

## Calibration Data

| T (°C) | avg ADC Raw | R_NTC (Ω) |
|--------|-------------|-----------|
| 29.6   | 762.0       | 7794      |
| 61.8   | 456.8       | 2146      |
| 85.5   | 280.0       | 1002      |

## Steinhart-Hart Coefficients

The coefficients were calculated from three reference temperature points
using nonlinear curve fitting based on the Steinhart-Hart model.

Calculated using the [Thermistor Calculator by Stanford Research Systems Inc](https://www.thinksrs.com/downloads/programs/therm%20calc/ntccalibrator/ntccalculator.html)
> **Note:** If the link is unavailable, coefficients can be recalculated using any
> Steinhart-Hart solver using the calibration data.

| Coefficient | Value        |
|-------------|--------------|
| A           | +7.927e-4    |
| B           | +3.015e-4    |
| C           | -2.659e-7    |

## Formula

$$\frac{1}{T} = A + B \cdot \ln(R) + C \cdot \ln(R)^3$$

## Results

- Max. deviation: ±0.5°C in the range 20–90°C
- Used ADC-Range: 254-842


