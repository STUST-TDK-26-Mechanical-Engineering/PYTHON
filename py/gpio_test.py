import Jetson.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
mode = GPIO.getmode()
print(mode)
channel=40
GPIO.setup(channel, GPIO.IN)
while 1:
    print(GPIO.input(channel))