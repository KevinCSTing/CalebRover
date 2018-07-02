#!/usr/bin/python
 
#import libraries we need
import random
import time #time library
import RPi.GPIO as GPIO
from picamera import PiCamera #import camera so we can record videos/ take snapshots
import time
import sys

GPIO.setmode(GPIO.BOARD)
#declare GPIO pins to be used for the wheels
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

# for the sensor
PIN_TRIGGER = 29 
PIN_ECHO = 31 
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN) 

dist = 0
tf = 1

def init():
    print dist
    turn = random.randint(1,2)
    print turn
    if dist >= 2:
	    left(2)
    else:
	    right(1)

def distance():
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    print "waiting for sensor to settle"
    time.sleep(2)

    print "calculating distance"
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO)==0:
       pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO) ==1:
       pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = pulse_duration * 34300/2
    print "distance: ", distance,"cm"
    #move(distance)
    return distance

def makeATurn():
    turn = random.randint(1,2)
    if turn == 1:
        return left(tf)
    else:
	    return right(tf)
		
#directions
def forward(tf):
    dist = distance()
    if dist > 5:
        print "forward"
        GPIO.output(7,False)
        GPIO.output(11,True)
        GPIO.output(13,True)
        GPIO.output(15,False)
        time.sleep(tf)
        GPIO.output(7,False)
        GPIO.output(11,False)
        GPIO.output(13,False)
        GPIO.output(15,False)
        GPIO.cleanup()
    else:
        print "reversing"
        reverse(tf)

def reverse(tf):
    GPIO.output(7,True)
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(15,True)
    time.sleep(tf)
    GPIO.cleanup()
    makeATurn()
	#random turn maybe?

def left(tf):
    print "turning left"
    GPIO.output(7,True)
    GPIO.output(11,False)
    GPIO.output(13,True)
    GPIO.output(15,False)
    time.sleep(tf)
    GPIO.cleanup()	

def right(tf):
    print "turning right"
    GPIO.output(7,False)
    GPIO.output(11,True)
    GPIO.output(13,False)
    GPIO.output(15,True)
    time.sleep(tf)
    GPIO.cleanup()

def stop(tf):
    print "stopping"
    GPIO.output(7,False)
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(15,False)
    GPIO.cleanup()	
init()
			