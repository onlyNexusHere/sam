import serial
import time

port = '/dev/cu.usbmodem14101'

ser = serial.Serial(port, 9600, timeout=2)


# print(ser.readline().decode('utf-8'))

mode = 0

m1 = 0

m2 = 100

motor_control = str(mode) + ' ' + str(m1) + ' ' + str(m2) + ' '

print(motor_control)

print("- - - - - - - -")

while True:
    ser.write(motor_control.encode())
    print(ser.readline().decode('utf-8'))
