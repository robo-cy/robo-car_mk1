#!/usr/bin/env python3
import warnings
from gpiozero import *
from gpiozero import PWMOutputDevice, DigitalOutputDevice, LED
from time import sleep
import curses

warnings.simplefilter('ignore')

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

#////////////////// Define LED Pins ///////////////////
Left_LED = LED(20)
Right_LED = LED(21)

#///////////////// Define Motor Driver GPIO Pins /////////////////
# Motor A, Left Side GPIO CONSTANTS
PWM_DRIVE_RIGHT = 18		# ENA - H-Bridge enable pin
RIGHT_DIR = 23	# IN1 - Forward Drive
# Motor B, Right Side GPIO CONSTANTS
PWM_DRIVE_LEFT = 12		# ENB - H-Bridge enable pin
LEFT_DIR = 16	# IN1 - Forward Drive

# Initialise objects for H-Bridge GPIO PWM pins
# Set initial duty cycle to 0 and frequency to 1000
driveLeft = PWMOutputDevice(PWM_DRIVE_LEFT, True, 0, 3000)
driveRight = PWMOutputDevice(PWM_DRIVE_RIGHT, True, 0, 3000)

# Initialise objects for H-Bridge digital GPIO pins
Leftdir = DigitalOutputDevice(LEFT_DIR)
Rightdir = DigitalOutputDevice(RIGHT_DIR)

def allStop():
    Leftdir.value = False
    Rightdir.value = False
    driveLeft.value = 0
    driveRight.value = 0

def forwardDrive():
    Leftdir.value = True
    Rightdir.value = True
    driveLeft.value = 0.5
    driveRight.value = 0.55

def spinLeft():
    Leftdir.value = False
    Rightdir.value = True
    driveLeft.value = 0.5
    driveRight.value = 0.5

def spinRight():
    Leftdir.value = True
    Rightdir.value = False
    driveLeft.value = 0.5
    driveRight.value = 0.5

def reverseDrive():
    Leftdir.value = False
    Rightdir.value = False
    driveLeft.value = 0.5
    driveRight.value = 0.55

def main():
    try:
        Left_LED.on()
        Right_LED.on()
        while True:
            k = screen.getch()
            if k == ord('q'):
                break
            elif k == curses.KEY_UP:
                print ("up")
                allStop()
                forwardDrive()
            elif k == curses.KEY_DOWN:
                print ("down")
                allStop()
                reverseDrive()
            elif k == curses.KEY_RIGHT:
                print ("right")
                allStop()
                spinRight()
            elif k == curses.KEY_LEFT:
                print ("left")
                allStop()
                spinLeft()
            elif k == ord('w'):
                print ("up")
                allStop()
                forwardDrive()
            elif k == ord('s'):
                print ("down")
                allStop()
                reverseDrive()
            elif k == ord('d'):
                print ("right")
                allStop()
                spinRight()
            elif k == ord('a'):
                print ("left")
                allStop()
                spinLeft()
            else:
                print ("Stopped...")
                allStop()
    except KeyboardInterrupt:
        print('Exiting...')
        close()
    finally:
        curses.nocbreak(); screen.keypad(0); curses.echo()
        curses.endwin()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
