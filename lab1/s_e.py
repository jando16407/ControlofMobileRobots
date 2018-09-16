import time
import Adafruit_PCA9685
import RPi.GPIO as GPIO
import signal
import math
import sys
import tty
import termios

# 0 represents the first servo, 1 for the second, and so on.
LSERVO = 0
RSERVO = 1

# Pins that the encoders are connected to
LENCODER = 17
RENCODER = 18

# Values to count ticks
left = 0
right = 0

# Values for getSpeed()
#global gtSp_Lstart, gtSp_Lstop, gtSp_Rstart, gtSp_Rstop, gtSp_Ltime_start, gtSp_Ltime_end, gtSp_Rtime_start, gtSp_Rtime_end
gtSp_Lstart = gtSp_Lstop = gtSp_Rstart = gtSp_Rstop = 0
gtSp_Rtime_start = gtSp_Rtime_end = gtSp_Ltime_start = gtSp_Ltime_end = 0

##########################
# This function is called when Ctrl+C is pressed.
# It's intended for properly exiting the program.
def ctrlC(signum, frame):
	print("Exiting")

	# Stop the servos
	pwm.set_pwm(LSERVO, 0, 0);
	pwm.set_pwm(RSERVO, 0, 0);

	exit()

# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)
#############################

# Initialize the servo hat library.
pwm = Adafruit_PCA9685.PCA9685()

# 50Hz is used for the frequency of the servos.
pwm.set_pwm_freq(50)

# The det_ch method will determine which key has been pressed
def det_ch():
	aa = sys.stdin.fileno()
	settings = termios.tcgetattr(aa)
	try:
		tty.setraw(sys.stdin.fileno())
		key = sys.stdin.read(1)
	finally:
		termios.tcsetattr(aa, termios.TCSADRAIN, settings)
	return key

# This function is called when the left encoder detects a rising edge signal.
def onLeftEncode(pin):
	global left
	left += 1
	display_ticks()
	check_elapsed_L()
	#if(gtSp_Lstart == 1):
	#	gtSp_Lstop = 1
	

def check_elapsed_L():
	global gtSp_Lstart, gtSp_Lstop, gtSp_Rstart, gtSp_Rstop, gtSp_Ltime_start, gtSp_Ltime_end, gtSp_Rtime_start, gtSp_Rtime_end
	if(gtSp_Lstop == 1):
		gtSp_Ltime_end = time.time()
		elapsed = gtSp_Ltime_end - gtSp_Ltime_start
		print("TIME ELAPSED IS : ", elapsed)
		gtSp_Lstart = gtSp_Lstop = 0
	if(gtSp_Lstart == 1):
		gtSp_Ltime_start = time.time()
#		gtSp_Ltime_start = 0
		gtSp_Lstop = 1
	

# This function is called when the right encoder detects a rising edge signal.
def onRightEncode(pin):
	global right
	right += 1
	display_ticks()

# This function displays current number of left and right ticks
def display_ticks():
	sys.stdout.write('\r')
	sys.stdout.write("Left encoder ticked! ")
	sys.stdout.write(str(left))
	sys.stdout.write(" : Right encoder ticked! ")
	sys.stdout.write(str(right))
	sys.stdout.flush()

# This function resets the tick count
def resetCounts():
	print("\nRESETCOUNTS CALLED")
	global left
	global right
	left = 0
	right = 0

# This function return the tuple of tick counts
def getCounts():
	print("\nGETCOUNTS CALLED")
	return (str(left), str(right))

# This function returns the current speed of servos
# def getSpeeds():d

# Set the pin numbering scheme to the numbering shown on the robot itself.
GPIO.setmode(GPIO.BCM)

# Set encoder pins as input
# Also enable pull-up resistors on the encoder pins
# This ensures a clean 0V and 3.3V is always outputted from the encoders.
GPIO.setup(LENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Attach a rising edge interrupt to the encoder pins
GPIO.add_event_detect(LENCODER, GPIO.RISING, onLeftEncode)
GPIO.add_event_detect(RENCODER, GPIO.RISING, onRightEncode)

# Write an initial value of 1.5, which keeps the servos stopped.
# Due to how servos work, and the design of the Adafruit library, 
# the value must be divided by 20 and multiplied by 4096.
pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096))
pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20* 4096))

# Prevent the program from exiting by adding a looping delay.
while True:
	# Write a maximum value of 1.7 for each servo.
    # Since the servos are oriented in opposite directions,
    # the robot will end up spinning in one direction.
    # Values between 1.3 and 1.7 should be used.

	key_input = det_ch()
	# get counts
	if key_input == "g":
		print(getCounts())
	# reset counts
	elif key_input == "r":
		resetCounts()
	# get current speed
	elif key_input == "t":
		print("GET CORRENT SPEED CALLED\n")
		gtSp_Lstart = gtSp_Rstart = 1
	# move forward
	elif key_input == "w":
		pwm.set_pwm(LSERVO, 0, math.floor(1.51 / 20 * 4096));
		pwm.set_pwm(RSERVO, 0, math.floor(1.49 / 20 * 4096));
	# move back
	elif key_input == "s":
		pwm.set_pwm(LSERVO, 0, math.floor(1.49 / 20 * 4096));
		pwm.set_pwm(RSERVO, 0, math.floor(1.51 / 20 * 4096));
	# turn right
	elif key_input == "d":
		pwm.set_pwm(LSERVO, 0, math.floor(1.51 / 20 * 4096));
		pwm.set_pwm(RSERVO, 0, math.floor(1.51 / 20 * 4096));
	# turn left
	elif key_input == "a":
		pwm.set_pwm(LSERVO, 0, math.floor(1.49 / 20 * 4096));
		pwm.set_pwm(RSERVO, 0, math.floor(1.49 / 20 * 4096));
	# stop
	elif key_input == "q":
		pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096));
		pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20 * 4096));
	# Exit the program
	elif key_input == "c":
		print("\nExiting")
		GPIO.cleanup()
		#Stop the servos
		pwm.set_pwm(LSERVO, 0, 0);
		pwm.set_pwm(RSERVO, 0, 0);
		exit()
