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
| 25.0   | 808.1       | 10000     |
| 61.8   | 456.8       |  2146     |
| 85.5   | 280.0       |  1002     |

## Steinhart-Hart Coefficients

The coefficients were calculated from three reference temperature points
using nonlinear curve fitting based on the Steinhart-Hart model.

Calculated using the [Thermistor Calculator by Stanford Research Systems Inc](https://www.thinksrs.com/downloads/programs/therm%20calc/ntccalibrator/ntccalculator.html)
> **Note:** If the link is unavailable, coefficients can be recalculated using any
> Steinhart-Hart solver using the calibration data.

| Coefficient | Value           |
|-------------|-----------------|
| A           | 0.7215939276e-3 |
| B           | 3.161853033e-4  |
| C           | -3.580517355e-7 |

## Formula

1/T = A + B·ln(R) + C·ln(R)³

## Results

- Max. deviation: ±0.5°C in the range 20–90°C
- Used ADC range: 254-842


