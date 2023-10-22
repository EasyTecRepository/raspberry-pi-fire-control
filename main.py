#!/usr/bin/env python
# Coding by Easy Tec | easytec.tech
# v5

import RPi.GPIO as GPIO
import multiprocessing
import signal
import time

# Set pin-number
PIN_output_BUZ = 18  # pin number for your output 1 (buzzer)
PIN_output_LED = 16  # pin number for your output 2 (LED)
PIN_b_alarm = 36  # pin number for your alarm button
PIN_b_reset = 37  # pin number for your reset button

GPIO.setmode(GPIO.BOARD)  # How to count the pins ("BOARD" or "BCM")

################################################################################

GPIO.setwarnings(False)  # Disable Warnings

# GPIO setup
GPIO.setup(PIN_output_BUZ, GPIO.OUT)
GPIO.setup(PIN_output_LED, GPIO.OUT)
GPIO.setup(PIN_b_alarm, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PIN_b_reset, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(PIN_output_BUZ, GPIO.LOW)
GPIO.output(PIN_output_LED, GPIO.LOW)

i = 0  # Set i to 0
reset = 0  # Set reset to 0

def DoIfAlarm():
    global i
    global reset
    while i == 0:
        GPIO.output(PIN_output_BUZ, GPIO.HIGH)
        GPIO.output(PIN_output_LED, GPIO.HIGH)
        print("Action: Alarm manually triggered")
        i = 1  # Set i to 1

    while GPIO.input(PIN_b_reset) == GPIO.LOW:
        time.sleep(0.1)
    while reset != 2:
        if (reset == 0) and (GPIO.input(PIN_b_reset) == GPIO.HIGH):
            DoIfMute()
            reset = 1  # Set reset to 1
            print("wait 2 seconds")
            time.sleep(2)
            print("waiting for interaction...")
        elif (reset == 1) and (GPIO.input(PIN_b_reset) == GPIO.HIGH):
            reset = 2  # Set reset to 2
            DoIfReset()

def DoIfMute():
    GPIO.output(PIN_output_BUZ, GPIO.LOW)
    print("Action: Alarm mute")

def DoIfReset():
    global i, reset
    GPIO.output(PIN_output_LED, GPIO.LOW)
    print("Action: Alarm reset")
    i = 0  # Set i to 0
    reset = 0  # Set reset to 0
    print("Reactivate system...")
    print("")
    MainLoop()  # Reactivate system
    StatusLight()  # Reactivate system

def StatusLight():
    global i
    while True:
        if i == 0:
            GPIO.output(PIN_output_LED, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(PIN_output_LED, GPIO.LOW)
            time.sleep(10)

def MainLoop():
    global reset
    print("System ready...")
    while True:
        if GPIO.input(PIN_b_alarm) == GPIO.HIGH:
            DoIfAlarm()
        time.sleep(0.1)
        if reset == 2:
            reset = 0
            break

def signal_handler(signal, frame):
    print("\nCleaning up...")
    GPIO.cleanup()
    # Stop threads
    thread_StatusLight.join()
    thread_MainLoop.join()
    thread_DoIfAlarm.join()
    thread_DoIfMute.join()
    thread_DoIfReset.join()
    exit(0)

# Create threads
thread_DoIfAlarm = multiprocessing.Process(target=DoIfAlarm)
thread_DoIfMute = multiprocessing.Process(target=DoIfMute)
thread_DoIfReset = multiprocessing.Process(target=DoIfReset)
thread_StatusLight = multiprocessing.Process(target=StatusLight)
thread_MainLoop = multiprocessing.Process(target=MainLoop)

# Start process
thread_StatusLight.start()
thread_MainLoop.start()
signal.signal(signal.SIGINT, signal_handler)
