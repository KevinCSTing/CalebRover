# import curses to control motors via keyboard
import curses
import time #time library
import RPi.GPIO as GPIO
import os #so we can do stuff like shutdown and restart
#import camera so we can record videos/ take snapshots
from picamera import PiCamera

#declare instance of picamera & rotate bec cam is upsidedown
camera = PiCamera()
camera.rotation = 180

GPIO.setmode(GPIO.BOARD)
#declare GPIO pins to be used
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

#get the curses window, turn off echoing of keyboard to screen,tur o
#instant (no waiting) key responses, and use special values for cursor keys
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        if char == ord('S'): #shutdown
            os.system('sudo shutdown -h now')
        if char == ord('R'): #restart
            os.system('sudo reboot')
        if char == ord('v'): #start recording
            print "start recording"
            camera.start_recording('/home/pi/Bobier/picsandvids/rovercams.h264')
        if char == ord('b'): #stop recording
            print "stop recording"
            camera.stop_recording()
        if char == ord('p'): #take pics
            print "picture taken"
            camera.capture('/home/pi/Bobier/picsandvids/roverstill.jpg')
        elif char == curses.KEY_UP:
            print "forward"
            GPIO.output(7,False)
            GPIO.output(11,True)
            GPIO.output(13,True)
            GPIO.output(15,False)
        elif char == curses.KEY_DOWN:
            print "reverse"
            GPIO.output(7,True)
            GPIO.output(11,False)
            GPIO.output(13,False)
            GPIO.output(15,True)
        elif char == curses.KEY_RIGHT:
            print "right"
            GPIO.output(7,False)
            GPIO.output(11,True)
            GPIO.output(13,False)
            GPIO.output(15,True)
        elif char == curses.KEY_LEFT:
            print "left"
            GPIO.output(7,True)
            GPIO.output(11,False)
            GPIO.output(13,True)
            GPIO.output(15,False)
        elif char == 10:
            print "stop"
            GPIO.output(7,False)
            GPIO.output(11,False)
            GPIO.output(13,False)
            GPIO.output(15,False)

finally:
    #close down curses properly, inc turn echo back on
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    GPIO.cleanup()
