#!/usr/bin/env python3


import warnings # Needed to be able to silence redundant error reports
from gpiozero import * # All the gpiozero modules allow us to control the
# raspberry pi GPIO pins
from gpiozero import PWMOutputDevice, DigitalOutputDevice, LED, DistanceSensor
from time import sleep # Allows us to tell our python program to pause for a specified time
import curses # Allows us to capture keypresses

warnings.simplefilter('ignore') # Ignore warnings

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

# Define LED Pins
Left_LED = LED(20)
Right_LED = LED(21)

# Define Motor Driver GPIO Pins 
# Motor A, Right Side GPIO CONSTANTS
PWM_DRIVE_RIGHT = 18		# Right H-Bridge enable pin
RIGHT_DIR = 23	# Right Forward Drive

# Motor B, Left Side GPIO CONSTANTS
PWM_DRIVE_LEFT = 12		# Left H-Bridge enable pin
LEFT_DIR = 16	# Left Forward Drive

sensor = DistanceSensor(echo=4, trigger=17, max_distance=1)
sense = 0
InRange = 0
powerlevel = 0

# Initialise objects for H-Bridge GPIO PWM pins
# Set initial duty cycle to 0 and frequency to 1000
driveLeft = PWMOutputDevice(PWM_DRIVE_LEFT, True, 0, 3000)
driveRight = PWMOutputDevice(PWM_DRIVE_RIGHT, True, 0, 3000)

# Initialise objects for H-Bridge digital GPIO pins
Leftdir = DigitalOutputDevice(LEFT_DIR)
Rightdir = DigitalOutputDevice(RIGHT_DIR)

# This function lets us control how close an object gets before evasive action is taken
def in_range(s):
    if s <= 30:
        return 1
    else:
        return 0

# This function lets us ease the power on or up
def rampup(n):
    global powerlevel
    for i in range(0, n):
        powerlevel = powerlevel + 0.1
        round(powerlevel, 1)
        if powerlevel < 0:
            powerlevel = 0
            driveRight.value = powerlevel
            driveLeft.value = powerlevel
        elif powerlevel > 1:
            powerlevel = 1
            driveRight.value = powerlevel
            driveLeft.value = powerlevel
        else:
            driveRight.value = powerlevel
            driveLeft.value = powerlevel
        sleep(0.05)

# This function lets us ease the power off or down
def rampdown(n):
    global powerlevel
    for i in range(0, n):
        powerlevel = powerlevel - 0.1
        round(powerlevel, 1)
        if powerlevel < 0:
            powerlevel = 0
            driveRight.value = powerlevel
            driveLeft.value = powerlevel
        elif powerlevel > 1:
            powerlevel = 1
            driveRight.value = powerlevel
            driveLeft.value = powerlevel
        else:
            driveRight.value = powerlevel
            driveLeft.value = powerlevel
        sleep(0.05)


def allStop():
    rampdown(11)

def forwardDrive():
    rampdown(6)
    Leftdir.value = True
    Rightdir.value = True
    rampup(5)

def spinLeft():
    rampdown(6)
    Leftdir.value = False
    Rightdir.value = True
    rampup(5)

def spinRight():
    rampdown(6)
    Leftdir.value = True
    Rightdir.value = False
    rampup(5)

def reverseDrive():
    rampdown(6)
    Leftdir.value = False
    Rightdir.value = False
    rampup(5)

def updaterange():
    global sense
    global InRange
    sense = sensor.distance * 100
    InRange = in_range(sense)

# This is where the main code is
# main() allows us to control the robot manually with either the arrow keys, or
# with the "a", "w", "s", and "d" keys
# "p" increases the powerlevel and "m" decreases the powerlevel
# if any other key is pressed we will stop
# if Ctrl + "c" is pressed we will switch over to auto()
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
                forwardDrive()
            elif k == curses.KEY_DOWN:
                print ("down")
                reverseDrive()
            elif k == curses.KEY_RIGHT:
                print ("right")
                spinRight()
            elif k == curses.KEY_LEFT:
                print ("left")
                spinLeft()
            elif k == ord('w'):
                print ("up")
                forwardDrive()
            elif k == ord('s'):
                print ("down")
                reverseDrive()
            elif k == ord('d'):
                print ("right")
                spinRight()
            elif k == ord('a'):
                print ("left")
                spinLeft()
            elif k == ord('p'):
                print ("faster")
                rampup(1)
            elif k == ord('m'):
                print ("slower")
                rampdown(1)
            else:
                print ("Stopped...")
                allStop()
    except KeyboardInterrupt:
        print('Auto Mode')
        auto()

# if Ctrl + "c" is pressed we will switch back to main()
def auto():
    try:
        Left_LED.blink()
        Right_LED.blink()
        while True:
            forwardDrive()
            sleep(0.01)
            print('Driving forward')
            print(sense)
            updaterange()
            while InRange:
                print(sense)
                spinLeft()
                print('Turning Left')
                sleep(0.2)
                updaterange()
    except KeyboardInterrupt:
        print('Manual mode')
        main()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
