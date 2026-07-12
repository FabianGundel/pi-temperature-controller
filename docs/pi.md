# PI Controller – Implementation & Tuning

## Control Architecture

A closed-loop feedback system where the controller continuously adjusts
PWM output based on the difference between setpoint and measured temperature.

---

## Why PI and not PID

A D-term was initially implemented but removed during tuning for two reasons:

- The water bath is a thermally slow system – temperature changes over
  seconds, not milliseconds. The D-term had no meaningful signal to act on.
- The NTC ADC signal contains residual noise even after capacitor filtering.
  The D-term amplified this noise, causing erratic PWM output.

A PI controller proved sufficient for stable and precise temperature regulation.

---

## Control Terms

**P – Proportional**
Drives output proportional to the current error. Provides the main
heating power during warm-up but cannot eliminate steady-state offset alone.

**I – Integral**
Accumulates error over time and eliminates steady-state offset.
Becomes the dominant term once the system approaches the setpoint.

---

## Anti-Windup

During warm-up the output is saturated at PWM = 255. Without anti-windup
the integral term accumulates during this phase and causes significant
overshoot once the setpoint is reached.

**Solution:** The integral only accumulates when the raw (unclamped) output
is within the valid range:

```cpp
double rawOutput = (Kp * errorPid) + (Ki * integral) + (Kd * derivative);

  if (rawOutput > 0 && rawOutput < 255) { 
    integral += errorPid * dt; 
    
    rawOutput = (Kp * errorPid) + (Ki * integral) + (Kd * derivative);
  } //integral only for finetuning

  
  previousError = errorPid;

  //pwm output
  output = constrain(rawOutput, 0, 255);
```

---

## Tuning

Tuning was performed by observing the temperature response curve using
a [custom live visualizer](../../tools/plotter/plotter.py).

### Approach

Starting point: Kp high enough to reach setpoint, Ki = 0.

Ki was increased gradually until steady-state offset was eliminated
without significant overshoot.

### Final Parameters

| Parameter | Value |
|-----------|-------|
| Kp        | x     |
| Ki        | x     |

### Response Curve

![Temperature Response](../../images/response.png)

---

## ADC Noise & Decoupling Capacitor

During calibration, significant jumps in ADC readings were observed
exclusively when the heating element was active.

**Root cause:** PWM switching causes rapid current transients through
the shared GND line. This induces brief voltage spikes that corrupt
the ADC reference, producing false temperature readings.

**Solution:** A 100nF decoupling capacitor between A0 and GND forms
an RC low-pass filter together with the NTC voltage divider, attenuating
high-frequency switching noise while passing the slow temperature signal.
