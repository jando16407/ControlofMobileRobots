import time
import Adafruit_PCA9685
import signal
import math
import sys
import tty
import termios

if sys.version[0]=="3" : raw_input=input
# The servo hat uses its own numbering scheme within the Adafruit library.
# 0 represents the first servo, 1 for the second, and so on.
LSERVO = 0
RSERVO = 1

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

# Write an initial value of 1.5, which keeps the servos stopped.
# Due to how servos work, and the design of the Adafruit library, 
# the value must be divided by 20 and multiplied by 4096.
pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096))
pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20* 4096))

#while True:
#	pwm.writePWMMicroseconds(1700)
#	delay(20)
#	RSERVO.writePWMMicroseconds(1300)
#	delay(20)

while True:
    # Write a maximum value of 1.7 for each servo.
    # Since the servos are oriented in opposite directions,
    # the robot will end up spinning in one direction.
    # Values between 1.3 and 1.7 should be used.
#	pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096));
#	pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20 * 4096));
#	time.sleep(0.02)

	key_input = det_ch()
	if key_input == "w":
		pwm.set_pwm(LSERVO, 0, math.floor(1.515 / 20 * 4096));
		pwm.set_pwm(RSERVO, 0, math.floor(1.485 / 20 * 4096));
	elif key_input == "s":
		pwm.set_pwm(LSERVO, 0, math.floor(1.485 / 20 * 4096));
		pwm.set_pwm(RSERVO, 0, math.floor(1.515 / 20 * 4096));
	elif key_input == "d":
		pwm.set_pwm(LSERVO, 0, math.floor(1.515 / 20 * 4096));
		pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20 * 4096));
	elif key_input == "a":
		pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096));
		pwm.set_pwm(RSERVO, 0, math.floor(1.485 / 20 * 4096));
	elif key_input == "q":
		pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096));
		pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20 * 4096));
	elif key_input == "c":
		print("Exiting")
		#Stop the servos
		pwm.set_pwm(LSERVO, 0, 0);
		pwm.set_pwm(RSERVO, 0, 0);
		exit()
    
		
    
    # Write a minimum value of 1.4 for each servo.
    # The robot will end up spinning in the other direction.
#    pwm.set_pwm(LSERVO, 0, math.floor(1.3 / 20 * 4096));
#    pwm.set_pwm(RSERVO, 0, math.floor(1.3 / 20 * 4096));
#    time.sleep(0.02)
