#!/usr/bin/python

#import libraries we need
import random
import time
import RPi.GPIO as GPIO
from picamera import PiCamera
import time

#set all GPIOS
GPIO.setmode(GPIO.BOARD)
#for the wheels
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

#for the sensor
PIN_TRIGGER = 29
PIN_ECHO = 31
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO,GPIO.IN)

#clear GPIOS
def clearGPIO():
    GPIO.output(7,False)
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(15,False)
    #GPIO.cleanup() #redundant but just to be sure

#driving directions
def forward():
    print "moving forward"
    GPIO.output(7,False)
    GPIO.output(11,True)
    GPIO.output(13,True)
    GPIO.output(15,False)

def reverse():
    print "reversing"
    GPIO.output(7,True)
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(15,True)
    time.sleep(0.8)
    GPIO.output(7,False)
    GPIO.output(15,False)

def right():
    print "turning right"
    GPIO.output(7,False)
    GPIO.output(11,True)
    GPIO.output(13,False)
    GPIO.output(15,True)
    time.sleep(0.8)
    GPIO.output(11,False)
    GPIO.output(15,False)	

def left():
    print "turning left"
    GPIO.output(7,True)
    GPIO.output(11,False)
    GPIO.output(13,True)
    GPIO.output(15,False)
    time.sleep(0.8)
    GPIO.output(7,False)
    GPIO.output(13,False)	
    
def stop():
    print "stopping"
    GPIO.output(7,False)
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(15,False)

def makeATurn():
    turn = random.randint(1,2)
    if turn == 1:
        return left()
    else:
        return right()

def distanceToObstacle():
    #set trigger to false
    GPIO.output(PIN_TRIGGER, False)
    print "waiting for sensor to settle"
    time.sleep(0.2)
    
    print "calculating distance"
    GPIO.output(PIN_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, False)

    while GPIO.input(PIN_ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(PIN_ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    # we only want the distance to the object so we divide the speed of sound in two
    distance = pulse_duration * 34000/2
    print "pulse duration: ",pulse_duration," seconds"
    print "distance: ", distance, "cm"
    return distance

def drive(dist):
    start = time.time()
    print dist," cm"
    #this will iterate everything under 60s
    while start > time.time() - 60:
        if distanceToObstacle() >= 10:
            forward()
        else:
            stop()
            time.sleep(0.8)           
            reverse()
            makeATurn()
            stop()

def main():
    clearGPIO()
    print "making my way downtown"
    #Start driving
    drive(distanceToObstacle())

if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()
