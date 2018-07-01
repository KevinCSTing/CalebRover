 #!/usr/bin/python
 
#import libraries we need
import random
import time #time library
import RPi.GPIO as GPIO
from picamera import PiCamera #import camera so we can record videos/ take snapshots
import time
import sys

#declare instance of picamera & rotate bec cam is upsidedown
camera = PiCamera()
camera.rotation = 180



def init():
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
    return

def forward(tf):
    print "forward"
    GPIO.output(7,False)
    GPIO.output(11,True)
    GPIO.output(13,True)
    GPIO.output(15,False)
    time.sleep(tf)
    GPIO.cleanup()

def reverse(tf):
    print "reverse"
    GPIO.output(7,True)
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(15,True)
    time.sleep(tf)
    GPIO.cleanup()

def left(tf):
    print "left"
    GPIO.output(7,True)
    GPIO.output(11,False)
    GPIO.output(13,True)
    GPIO.output(15,False)
    time.sleep(tf)
    GPIO.cleanup()
  
def right(tf):
    print "right"
    GPIO.output(7,False)
    GPIO.output(11,True)
    GPIO.output(13,False)
    GPIO.output(15,True)
    time.sleep(tf)
    GPIO.cleanup()

def stop(tf):
    print "stop"
    GPIO.output(7,False)
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(15,False)
    GPIO.cleanup()


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
    distance = round(pulse_duration / 0.000148, 2)
    print "distance: ", distance,"in"
    return
  
def check_sensor():
    init()
    dist = distance()

    if dist < 15:
        print('too close,' ,dist)
        init()
        reverse(1)
        dist = distance()
    if dist < 15:
            print('too close,' ,dist)
            init()
            left(3)
            init()
            reverse(1)
            dist = distance()
            if dist <15:
                print('too close, giving up. goodbye')
                sys.exit()
        
def autonomy():
    tf = 0.030
    x = random.randrange(0,4)

    if x == 0:
      for y in range(30):
        check_sensor()
        init()
        forward(tf)
    elif x == 1:
        for y in range(30):
            check_sensor()
            init()
            left(tf)
    elif x == 2:
        for y in range(30):
            check_sensor()
            init()
            left(tf)
    elif x == 3:
        for y in range(30):
            check_sensor()
            init()
            right(tf)

init()

for z in range(10):
    autonomy()
      