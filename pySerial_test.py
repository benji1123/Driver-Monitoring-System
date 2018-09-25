import serial
arduino= serial.Serial('/dev/cu.usbmodem14411', 9600, timeout = 0)
while True:
    if (arduino.inWaiting()>0):
        wheel_score = arduino.readline().decode('ascii')
        print(wheel_score)
