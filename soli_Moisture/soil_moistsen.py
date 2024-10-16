import RPi.GPIO as GPIO
import time

# Set the GPIO pin for the digital sensor
MOISTURE_SENSOR_PIN = 17

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOISTURE_SENSOR_PIN, GPIO.IN)

try:
    while True:
        # Read the moisture level
        if GPIO.input(MOISTURE_SENSOR_PIN):
            print("Soil is wet!")
        else:
            print("Soil is dry!")

        time.sleep(1)  # Wait for a second before reading again

except KeyboardInterrupt:
    print("Program stopped.")

finally:
    GPIO.cleanup()  # Clean up GPIO settings
