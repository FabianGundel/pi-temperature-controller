import serial
import requests

SERVER_URL = "" #localhostURL + /data
BAUD_RATE = 9600 
COM_PORT = "COM4" #Change to your COM port

ser = serial.Serial(COM_PORT, BAUD_RATE)

while True:
    line = ser.readline().decode().strip()

    requests.post(
        SERVER_URL,
        json={"value": line}
    )