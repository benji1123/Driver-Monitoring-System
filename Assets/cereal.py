import serial
import time

PORT = "COM3"
RATE = 9600

MOVE_LEFT  = 'l'
MOVE_RIGHT = 'r'

# Establish Servo-Cnxn & Controls
def move_left():
    if(connected):
        ser.write(MOVE_LEFT.encode())
def move_right():
    if(connected):
        ser.write(MOVE_RIGHT.encode())
connected = False
ser = serial.Serial(PORT, RATE)

while(not(connected)):
    serin = ser.read()
    connected = True

while(True):
	for n in range(4):
		move_left()
		time.sleep(0.3)

	for n in range(4):
		move_right()
		time.sleep(0.3)

ser.close()