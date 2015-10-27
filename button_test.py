from smbus import  SMBus
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

print "Press and release the button"

GPIO.wait_for_edge(24, GPIO.RISING)

print "Pressed"

GPIO.wait_for_edge(24, GPIO.FALLING)

print "Released"

