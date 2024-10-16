import time
import board
import adafruit_dht
import csv
from datetime import datetime
import busio
from adafruit_bh1750 import BH1750  # Lux sensor
import adafruit_bmp280  # Air pressure sensor
import digitalio  # For soil moisture sensor

# Define the pins where the sensors are connected
DHT_PIN = board.D4  # Change this to your pin
SOIL_MOISTURE_PIN = board.D18  # Change this to your analog pin for soil moisture

# Create instances for the sensors
dht_sensor = adafruit_dht.DHT11(DHT_PIN)  # or adafruit_dht.DHT22(DHT_PIN)
i2c = busio.I2C(board.SCL, board.SDA)  # Update with your board's SCL and SDA
lux_sensor = BH1750(i2c)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)  # BMP280 for air pressure

def read_pkn():
    # Hypothetical code to read from the PKN sensor
    # Replace this with your actual reading logic
    pkn_value = 42  # Example PKN value
    return pkn_value

# Open a CSV file to write the data
with open('sensorData.csv', mode='w', newline='') as csvfile:
    fieldnames = [
        'Timestamp', 
        '   Temperature (°C)', 
        '   Humidity (%)', 
        '   Max Temperature (°C)', 
        '   Min Temperature (°C)', 
        '   Max Humidity (%)', 
        '   Min Humidity (%)',
        '   Lux (lx)', 
        '   PKN (units)',  # Update with the actual unit for PKN
        '   Soil Moisture (%)', 
        '   Air Pressure (hPa)'
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Initialize max and min values
    max_temperature = float('-inf')
    min_temperature = float('inf')
    max_humidity = float('-inf')
    min_humidity = float('inf')

    try:
        while True:
            current_time = datetime.now()
            hour = current_time.hour

            # Check if it's morning (8 AM), lunch (12 PM), or night (8 PM)
            if hour == 8 or hour == 12 or hour == 20:
                try:
                    # Read temperature and humidity from the DHT sensor
                    temperature_c = dht_sensor.temperature
                    humidity = dht_sensor.humidity

                    # Read lux from the lux sensor
                    lux = lux_sensor.lux

                    # Read PKN value
                    pkn = read_pkn()  # Get PKN value
                    print(f'PKN: {pkn}')  # Print PKN value individually

                    # Read soil moisture from the soil moisture sensor
                    soil_moisture = digitalio.DigitalInOut(SOIL_MOISTURE_PIN)
                    soil_moisture_percentage = (soil_moisture.value / 65535) * 100  # Convert to percentage

                    # Read air pressure from the BMP280 sensor
                    air_pressure = bmp280.pressure  # in hPa

                    if humidity is not None and temperature_c is not None and lux is not None:
                        # Print the data to console
                        print(f'Temperature: {temperature_c}°C  Humidity: {humidity}%  Lux: {lux}lx  PKN: {pkn}  Soil Moisture: {soil_moisture_percentage:.2f}%  Air Pressure: {air_pressure:.2f}hPa')

                        # Update max and min temperature
                        if temperature_c > max_temperature:
                            max_temperature = temperature_c
                        if temperature_c < min_temperature:
                            min_temperature = temperature_c

                        # Update max and min humidity
                        if humidity > max_humidity:
                            max_humidity = humidity
                        if humidity < min_humidity:
                            min_humidity = humidity

                        # Get the current timestamp
                        timestamp = current_time.isoformat()

                        # Write the data to the CSV file
                        writer.writerow({
                            'Timestamp': timestamp,
                            '   Temperature (°C)': f' {temperature_c} ',
                            '   Humidity (%)': f' {humidity} ',
                            '   Max Temperature (°C)': f' {max_temperature} ',
                            '   Min Temperature (°C)': f' {min_temperature} ',
                            '   Max Humidity (%)': f' {max_humidity} ',
                            '   Min Humidity (%)': f' {min_humidity} ',
                            '   Lux (lx)': f' {lux} ',
                            '   PKN (units)': f' {pkn} ',  # Include PKN in CSV
                            '   Soil Moisture (%)': f' {soil_moisture_percentage:.2f} ',
                            '   Air Pressure (hPa)': f' {air_pressure:.2f} '
                        })

                        # Optionally flush the writer to ensure data is written immediately
                        csvfile.flush()

                    else:
                        print('Failed to read data from the sensors.')

                except Exception as e:
                    print(f'Error reading from sensors: {e}')

                # Wait for an hour before the next reading
                time.sleep(3600)
            else:
                # Sleep for a while before checking the time again
                time.sleep(60)

    except KeyboardInterrupt:
        print("Exiting the program.")
