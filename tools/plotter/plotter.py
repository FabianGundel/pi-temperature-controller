import json
import os
import re
import urllib.request

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib.animation as animation
import matplotlib.pyplot as plt

SERVER_URL = "" #localhostURL + /latest
UPDATE_INTERVAL = 2000 #update in ms

times = []
temperatures = []
setpoints = []

figure, axis = plt.subplots()


def parse_pid_line(line):
    if isinstance(line, dict):
        line = line.get("value", line.get("raw", line.get("data", "")))

    line = str(line).strip()

    setpoint_match = re.search(
        r"(?:Soll|Setpoint)\s*:\s*(-?\d+(?:[.,]\d+)?)",
        line,
        re.IGNORECASE,
    )
    actual_match = re.search(
        r"(?:Ist|Process)\s*:\s*(-?\d+(?:[.,]\d+)?)",
        line,
        re.IGNORECASE,
    )

    if setpoint_match and actual_match:
        setpoint_temperature = float(setpoint_match.group(1).replace(",", "."))
        actual_temperature = float(actual_match.group(1).replace(",", "."))
        return setpoint_temperature, actual_temperature

    actual_temperature = float(line.replace(",", "."))
    setpoint_temperature = None
    return setpoint_temperature, actual_temperature


def parse_value(line, label):
    match = re.search(
        rf"{label}\s*:\s*(-?\d+(?:[.,]\d+)?)",
        str(line),
        re.IGNORECASE,
    )

    if not match:
        return None

    return float(match.group(1).replace(",", "."))


def parse_points_from_values(values):
    points = []
    current = {}

    def add_current_point():
        if "setpoint" not in current or "actual" not in current:
            return

        point = {
            "time": len(points),
            "setpoint": current["setpoint"],
            "actual": current["actual"],
        }

        if "pwm" in current:
            point["pwm"] = current["pwm"]

        if "error" in current:
            point["error"] = current["error"]

        points.append(point)

    for line in values:
        line = str(line).strip()

        if not line or set(line) == {"-"}:
            add_current_point()
            current = {}
            continue

        setpoint = parse_value(line, "Setpoint")
        if setpoint is not None:
            current["setpoint"] = setpoint
            continue

        actual = parse_value(line, "Process")
        if actual is not None:
            current["actual"] = actual
            continue

        pwm = parse_value(line, "PWM")
        if pwm is not None:
            current["pwm"] = pwm
            continue

        error = parse_value(line, "Error")
        if error is not None:
            current["error"] = error
            continue

        try:
            setpoint_temperature, actual_temperature = parse_pid_line(line)
            point = {
                "time": len(points),
                "actual": actual_temperature,
            }

            if setpoint_temperature is not None:
                point["setpoint"] = setpoint_temperature

            points.append(point)
        except ValueError:
            pass

    add_current_point()
    return points


def load_points_from_server():
    with urllib.request.urlopen(SERVER_URL, timeout=2) as response:
        data = json.loads(response.read().decode("utf-8"))

    if data.get("points"):
        return data["points"]

    raw_values = data.get("values", [])
    if not raw_values and "value" in data:
        raw_values = [data["value"]]

    return parse_points_from_values(raw_values)


def update(frame):
    try:
        points = load_points_from_server()
    except Exception as error:
        axis.clear()
        axis.set_title(f"Server down: {error}")
        return

    if not points:
        axis.clear()
        axis.set_title("Waiting for data")
        return

    times[:] = [point["time"] for point in points]
    temperatures[:] = [point["actual"] for point in points]
    setpoints[:] = [point.get("setpoint") for point in points]

    axis.clear()
    axis.plot(times, temperatures, label="Actual")
    if any(setpoint is not None for setpoint in setpoints):
        setpoint_times = [
            point["time"]
            for point in points
            if point.get("setpoint") is not None
        ]
        setpoint_values = [
            point["setpoint"]
            for point in points
            if point.get("setpoint") is not None
        ]
        axis.plot(setpoint_times, setpoint_values, "--", label="Setpoint")

    axis.set_xlabel("Zeit / Messpunkt")
    axis.set_ylabel("Temperature (C)")
    axis.legend()
    axis.grid(True)


if __name__ == "__main__":
    live_plot = animation.FuncAnimation(
        figure,
        update,
        interval=UPDATE_INTERVAL,
        cache_frame_data=False,
    )
    plt.show()
