import time
import RPi.GPIO as GPIO
import signal
import sys
import tty
import termios

# Pins that the encoders are connected to
LENCODER = 17
RENCODER = 18
left = 0
right = 0

# declare tuple
#counts = ("Left count : ", str(left), ", RIght count : ", str(right));

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


# This function is called when Ctrl+C is pressed.
# It's intended for properly exiting the program.
def ctrlC(signum, frame):
	print(str(left))
	print("\n", str(right))
	print("\nExiting")
	GPIO.cleanup()
	exit()

# This function resets the tick count
def resetCounts():
	print("RESETCOUNTS CALLED")
	global left
	global right
	left = 0
	right = 0

# This function return the tuple of tick counts
def getCounts():
	print("GETCOUNTS CALLED\n")
	return (str(left), str(right))

# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)
    
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

# Prevent the program from exiting by adding a looping delay.
while True:
	time.sleep(1)
	key_input = det_ch()
	if key_input == "g":
		print(getCounts())
	elif key_input == "r":
		resetCounts()
	elif key_input == "c":
		GPIO.cleanup()
		print("Exiting")
		exit()
