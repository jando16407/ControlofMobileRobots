import time
import RPi.GPIO as GPIO
import signal
import sys

# Pins that the encoders are connected to
LENCODER = 17
RENCODER = 18
left = 0
right = 0
# This function is called when the left encoder detects a rising edge signal.
def onLeftEncode(pin):
	global left
	left += 1
	sys.stdout.write('\r')
	sys.stdout.write("Left  encoder ticked! ")
	sys.stdout.write(str(left))
	sys.stdout.flush()
#	print("\r")
#	print("Left encoder ticked!")
#	print(str(left))

# This function is called when the right encoder detects a rising edge signal.
def onRightEncode(pin):
	global right
	right += 1
	print("Right encoder ticked!")

# This function is called when Ctrl+C is pressed.
# It's intended for properly exiting the program.
def ctrlC(signum, frame):
	print(str(left))
	print("\n", str(right))
	print("\nExiting")
	GPIO.cleanup()
	exit()

# This function resets the tick count
def resetCouns():


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
