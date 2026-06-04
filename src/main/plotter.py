import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

baudrate = 9600

serial_connection = serial.Serial('/dev/ttyUSB0', baudrate)  

times = []
temperatures = []
setpoints = []
start_time = None

figure, axis = plt.subplots()

def update(frame):
    serial_line = serial_connection.readline().decode('utf-8').strip()
    # matches your Serial.print format:
    # "Soll: 50.0 C | Ist: 23.4 C | PWM: 200 | Fehler: 26.6"
    try:
        fields = serial_line.split('|')
        actual_temperature = float(fields[1].split(':')[1].replace('C','').strip())
        setpoint_temperature = float(fields[0].split(':')[1].replace('C','').strip())
        
        import time
        global start_time
        if start_time is None:
            start_time = time.time()
        
        times.append((time.time() - start_time) / 60)  # minutes
        temperatures.append(actual_temperature)
        setpoints.append(setpoint_temperature)
        
        axis.clear()
        axis.plot(times, temperatures, label='Actual')
        axis.plot(times, setpoints, '--', label='Setpoint')
        axis.set_xlabel('Time (min)')
        axis.set_ylabel('Temperature (°C)')
        axis.legend()
        axis.grid(True)
    except:
        pass

live_plot = animation.FuncAnimation(figure, update, interval=500)
plt.show()