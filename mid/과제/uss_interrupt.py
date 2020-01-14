#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
from threading import Timer,Thread,Event

TRIG = 11
ECHO = 12
echo_start = 0
pre_dis = 0
case_cnt = 0

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

def my_interrupt(ECHO):
    if GPIO.input(ECHO):	# ECHO rising
        global echo_start
        echo_start  = time.time()
    else:	# ECHO falling
        echo_during = time.time() - echo_start
        if echo_during <= 0.03: # get distance
            global pre_dis
            dis =  echo_during * 340 / 2 * 100
            pre_dis = dis
            print "count:", case_cnt, ", ", "  ", ", distance:", dis
        else:	# time out
            print "count:", case_cnt, ", ", "TO", ", distance:", pre_dis

def trigger():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    if GPIO.input(ECHO):	# still ECHO = 1
        print "count:", case_cnt, ", ", "NR", ", distance:", pre_dis
    else:	# ECHO = 0
        GPIO.output(TRIG, 1)
        time.sleep(0.00001)
        GPIO.output(TRIG, 0)

def loop():
    loop_start = time.time()
    while time.time() - loop_start <= 60:
        distance_start = time.time()
        global case_cnt
        case_cnt += 1
        trigger()
        distance_during = 0.05 - (time.time() - distance_start)
        time.sleep(distance_during)

def destroy():
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    GPIO.add_event_detect(ECHO, GPIO.BOTH, callback=my_interrupt)
    try:
        loop()
    except KeyboardInterrupt:
        destroy()