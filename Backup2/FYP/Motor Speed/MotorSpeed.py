import RPi.GPIO as GPIO
from gpiozero import PWMOutputDevice
import time

pwmPin = PWMOutputDevice(25)
pwmPin.frequency = 1000
pwmPin.value = 0.99 #0.01 to 0.99

in1 = 23
in2 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.LOW)

init()
time.sleep(10)

print("Terminating")
GPIO.cleanup()