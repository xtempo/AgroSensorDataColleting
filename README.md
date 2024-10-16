# AgroSensorDataColleting


# Run the Python Script

# Make sure the script is executable (if necessary):

  chmod +x your_script.py

# Run the script:

  python3 your_script.py






# If you are using main.py then you have chech 
# Ensure I2C is Enabled

#Make sure that I2C is enabled on your Raspberry Pi:

   1. Run sudo raspi-config.
   2. Navigate to Interfacing Options > I2C and enable it.
   3. Reboot your Raspberry Pi.


# To Troubleshooting the I2C

# If you encounter any issues with I2C, ensure your connections are correct and that   the sensor is powered.

# You can check if the TSL2561 is detected on the I2C bus by running:

  sudo i2cdetect -y 1

# Look for the address of the TSL2561, which is typically 0x39.

# This setup will allow you to read light levels from the TSL2561 sensor using       
  Python on your Raspberry Pi.
