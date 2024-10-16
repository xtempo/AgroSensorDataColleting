import time
import board
import adafruit_dht
import adafruit_tsl2561
import csv
from datetime import datetime
import digitalio
import random  # For simulating PKN values

class SensorApp:
    def __init__(self):
        # Define the pins where the sensors are connected
        self.DHT_PIN = board.D4  # DHT sensor pin
        self.SOIL_MOISTURE_PIN = board.D17  # Soil moisture sensor pin
        self.SMOKE_SENSOR_PIN = board.D18  # Smoke sensor pin

        # Create instances for the sensors
        self.dht_sensor = adafruit_dht.DHT11(self.DHT_PIN)
        self.smoke_sensor = digitalio.DigitalInOut(self.SMOKE_SENSOR_PIN)
        self.smoke_sensor.direction = digitalio.Direction.INPUT
        self.soil_moisture_sensor = digitalio.DigitalInOut(self.SOIL_MOISTURE_PIN)
        self.soil_moisture_sensor.direction = digitalio.Direction.INPUT

        # Set up the lux sensor (TSL2561)
        self.i2c = board.I2C()  # Create I2C bus
        self.lux_sensor = adafruit_tsl2561.TSL2561(self.i2c)
        self.lux_sensor.enabled = True  # Enable the sensor

        # Set up the CSV file
        self.csvfile = open('sensorData.csv', mode='w', newline='')
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.get_fieldnames())
        self.writer.writeheader()

        # Initialize max and min values
        self.max_temperature = float('-inf')
        self.min_temperature = float('inf')
        self.max_humidity = float('-inf')
        self.min_humidity = float('inf')

        # Initialize sensor connection status
        self.dht_connected = True
        self.lux_connected = True
        self.smoke_connected = True
        self.soil_moisture_connected = True

    def get_fieldnames(self):
        return [
            'Timestamp', 
            'Temperature (°C)', 
            'Humidity (%)', 
            'Max Temperature (°C)', 
            'Min Temperature (°C)', 
            'PKN (units)',  
            'Soil Moisture (%)', 
            'Smoke Detected', 
            'Lux (lux)'
        ]

    def read_dht_sensor(self):
        try:
            temperature = self.dht_sensor.temperature
            humidity = self.dht_sensor.humidity
            return temperature, humidity
        except Exception:
            print("DHT sensor not connected or failed to read.")
            self.dht_connected = False  # Mark as disconnected
            return None, None

    def read_soil_moisture(self):
        try:
            return self.soil_moisture_sensor.value  # Returns True (wet) or False (dry)
        except Exception:
            print("Soil moisture sensor not connected or failed to read.")
            self.soil_moisture_connected = False  # Mark as disconnected
            return None

    def read_smoke_sensor(self):
        try:
            return self.smoke_sensor.value  # Returns True (smoke detected) or False (no smoke)
        except Exception:
            print("Smoke sensor not connected or failed to read.")
            self.smoke_connected = False  # Mark as disconnected
            return None

    def read_pkn(self):
        try:
            pkn_value = self.get_pkn_value()  # Replace with actual sensor reading logic
            return pkn_value
        except Exception as e:
            print(f"Error reading from PKN sensor: {e}")
            return None

    def get_pkn_value(self):
        # Simulating a PKN value for demonstration
        return random.uniform(0, 100)  # Replace with actual sensor reading logic

    def read_lux(self):
        try:
            lux = self.lux_sensor.lux
            return lux
        except Exception as e:
            print(f"Error reading from lux sensor: {e}")
            self.lux_connected = False  # Mark as disconnected
            return None

    def log_data(self):
        while True:
            current_time = datetime.now()
            print(f"Current time: {current_time.isoformat()}", flush=True)

            temperature, humidity = self.read_dht_sensor() if self.dht_connected else (None, None)
            pkn = self.read_pkn()  # Assuming PKN is always present
            soil_moisture = self.read_soil_moisture() if self.soil_moisture_connected else None
            smoke_detected = self.read_smoke_sensor() if self.smoke_connected else None
            lux = self.read_lux() if self.lux_connected else None

            # Print the data to the console
            print(f'Temperature: {temperature if self.dht_connected else "N/A"}°C  '
                  f'Humidity: {humidity if self.dht_connected else "N/A"}%  '
                  f'PKN: {pkn}  '
                  f'Soil Moisture: {soil_moisture if self.soil_moisture_connected else "N/A"}%  '
                  f'Smoke Detected: {"Yes" if smoke_detected else "No"}  '
                  f'Lux: {lux if self.lux_connected else "N/A"} lux', flush=True)

            # Get the current timestamp
            timestamp = current_time.isoformat()

            # Write the data to the CSV file
            self.writer.writerow({
                'Timestamp': timestamp,
                'Temperature (°C)': f'{temperature}' if self.dht_connected else 'N/A',
                'Humidity (%)': f'{humidity}' if self.dht_connected else 'N/A',
                'Max Temperature (°C)': f'{self.max_temperature:.2f}',
                'Min Temperature (°C)': f'{self.min_temperature:.2f}',
                'PKN (units)': f'{pkn}',
                'Soil Moisture (%)': f'{soil_moisture if self.soil_moisture_connected else "N/A"}',
                'Smoke Detected': 'Yes' if smoke_detected else 'No',
                'Lux (lux)': f'{lux}' if self.lux_connected else 'N/A'
            })

            self.csvfile.flush()
            time.sleep(10)  # Wait for 10 seconds before the next reading

    def close(self):
        self.csvfile.close()
        print("Exiting the program.")

if __name__ == '__main__':
    app = SensorApp()
    try:
        app.log_data()
    except KeyboardInterrupt:
        app.close()
