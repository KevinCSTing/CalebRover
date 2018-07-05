#source: https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

import threading, time, sys
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
PIN_TRIGGER = 29 
PIN_ECHO = 31 

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN) 

def distance():
    GPIO.output(PIN_TRIGGER, False)
    print "waiting for sensor to settle"
    time.sleep(2)

    print "calculating distance"
    GPIO.output(PIN_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, False)

    while GPIO.input(PIN_ECHO)==0:
       pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO) ==1:
       pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    print "pulse duration: ", pulse_duration    
    distance = pulse_duration * 17150 # 34300 m/s is speed of sound. we cut it in half because we just want the distance to the object
    print "pulse start: ", pulse_start_time
    print "pulse end: ", pulse_end_time
    print "distance: ", distance,"cm"
    #move(distance)
    GPIO.cleanup()
    return distance 
 
class counter :
    
    def getDistance(self):
        distFlag = int(round(distance()))#round to nearest whole number
        print "distance: ", distFlag
        for i in range (distFlag,0,-1):#decrement. consume distance
            print(i)
            if distFlag <= 12: #stop rover and reverse if sensor detects obstacle 12cm or 5 inches away
			    break
            time.sleep(.01)#speed of decrement
 
    def move(self):
        print(' Processing .. ')
        time.sleep(3)
  

 
th1 = threading.Thread(target = counter().getDistance).start()
th2 = threading.Thread(target = counter().move).start()