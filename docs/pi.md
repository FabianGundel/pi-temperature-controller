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

## Challenges during parameter tuning

During the tuning process some anomalies occured that requiered the implementation of further elements into the basic PI-Controller in order to solve those problems.

### Feedforward Offset

At the target temperature of 35°C the system requires approximately
150/255 PWM just to compensate for heat loss to the environment.
A standard PI controller would need to accumulate a large integral
term to provide this base load, causing slow response and overshoot.

To solve this, a fixed feedforward offset is added directly to the
controller output:

```cpp
rawOutput = offset + (Kp * errorPid) + (Ki * integral);
```

This allows the PI controller to operate only around the deviation
from the steady-state operating point, enabling much smaller Kp and
Ki values and significantly reducing integral windup.

### Anti-Windup

The integral term is only active within a defined error threshold
around the setpoint:

```cpp
if (abs(errorPid) < integralCap) {
    integral += errorPid * dt;
}
```

During the heating phase the proportional term and feedforward offset
provide sufficient output to drive the temperature toward the setpoint.
Accumulating the integral during this phase would cause significant
overshoot once the setpoint is reached.

By activating the integral only within the threshold, it starts from
zero when the system enters the fine control region – eliminating the
steady-state offset left by the P-term without the risk of windup.

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
| Kp        | 18.0  |
| Ki        | 0.01  |

---


