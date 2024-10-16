import time
import board
import adafruit_dht
import adafruit_tsl2561
import csv
from datetime import datetime
import digitalio
import random  # For simulating gas concentrations and pH values

class SensorApp:
    def __init__(self):
        # Define the pins where the sensors are connected
        self.DHT_PIN = board.D4  # DHT sensor pin
        self.SOIL_MOISTURE_PIN = board.D17  # Soil moisture sensor pin
        self.SMOKE_SENSOR_PIN = board.D18  # Smoke sensor pin
        self.PH_SENSOR_PIN = board.A0  # Analog pin for pH sensor (example)

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
            'Lux (lux)',
            'Alcohol (ppm)',
            'Ammonia (ppm)',
            'Benzene (ppm)',
            'CO2 (ppm)',
            'Smoke (ppm)',
            'pH Level',
            'pH Condition'
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

    def read_gas_concentrations(self):
        # Simulated gas concentrations for demonstration
        alcohol_ppm = random.uniform(0, 1000)
        ammonia_ppm = random.uniform(0, 500)
        benzene_ppm = random.uniform(0, 300)
        co2_ppm = random.uniform(0, 1500)
        smoke_ppm = random.uniform(0, 600)

        return {
            'Alcohol': alcohol_ppm,
            'Ammonia': ammonia_ppm,
            'Benzene': benzene_ppm,
            'CO2': co2_ppm,
            'Smoke': smoke_ppm
        }

    def read_lux(self):
        try:
            lux = self.lux_sensor.lux
            return lux
        except Exception as e:
            print(f"Error reading from lux sensor: {e}")
            self.lux_connected = False  # Mark as disconnected
            return None

    def read_ph_sensor(self):
        # Simulated pH reading (replace with actual pH sensor reading logic)
        pH_value = random.uniform(0, 14)  # pH scale typically ranges from 0 to 14
        return pH_value

    def get_ph_condition(self, ph_value):
        if ph_value < 7:
            return "Acidic"
        elif ph_value == 7:
            return "Neutral"
        else:
            return "Basic"

    def log_data(self):
        while True:
            current_time = datetime.now()
            print(f"Current time: {current_time.isoformat()}", flush=True)

            temperature, humidity = self.read_dht_sensor() if self.dht_connected else (None, None)
            soil_moisture = self.read_soil_moisture() if self.soil_moisture_connected else None
            smoke_detected = self.read_smoke_sensor() if self.smoke_connected else None
            lux = self.read_lux() if self.lux_connected else None
            
            # Read gas concentrations
            gas_levels = self.read_gas_concentrations()
            alcohol_ppm = gas_levels['Alcohol']
            ammonia_ppm = gas_levels['Ammonia']
            benzene_ppm = gas_levels['Benzene']
            co2_ppm = gas_levels['CO2']
            smoke_ppm = gas_levels['Smoke']

            # Read pH level
            ph_value = self.read_ph_sensor()
            ph_condition = self.get_ph_condition(ph_value)

            # Print the data to the console
            print(f'Temperature: {temperature if self.dht_connected else "N/A"}°C  '
                  f'Humidity: {humidity if self.dht_connected else "N/A"}%  '
                  f'Soil Moisture: {soil_moisture if self.soil_moisture_connected else "N/A"}%  '
                  f'Smoke Detected: {"Yes" if smoke_detected else "No"}  '
                  f'Lux: {lux if self.lux_connected else "N/A"} lux  '
                  f'Alcohol: {alcohol_ppm:.2f} ppm  '
                  f'Ammonia: {ammonia_ppm:.2f} ppm  '
                  f'Benzene: {benzene_ppm:.2f} ppm  '
                  f'CO2: {co2_ppm:.2f} ppm  '
                  f'Smoke Gas: {smoke_ppm:.2f} ppm  '
                  f'pH Level: {ph_value:.2f}  '
                  f'pH Condition: {ph_condition}', flush=True)

            # Get the current timestamp
            timestamp = current_time.isoformat()

            # Write the data to the CSV file
            self.writer.writerow({
                'Timestamp': timestamp,
                'Temperature (°C)': f'{temperature}' if self.dht_connected else 'N/A',
                'Humidity (%)': f'{humidity}' if self.dht_connected else 'N/A',
                'Max Temperature (°C)': f'{self.max_temperature:.2f}',
                'Min Temperature (°C)': f'{self.min_temperature:.2f}',
                'PKN (units)': random.uniform(0, 100),  # Simulated PKN value
                'Soil Moisture (%)': f'{soil_moisture if self.soil_moisture_connected else "N/A"}',
                'Smoke Detected': 'Yes' if smoke_detected else 'No',
                'Lux (lux)': f'{lux}' if self.lux_connected else 'N/A',
                'Alcohol (ppm)': f'{alcohol_ppm:.2f}',
                'Ammonia (ppm)': f'{ammonia_ppm:.2f}',
                'Benzene (ppm)': f'{benzene_ppm:.2f}',
                'CO2 (ppm)': f'{co2_ppm:.2f}',
                'Smoke (ppm)': f'{smoke_ppm:.2f}',
                'pH Level': f'{ph_value:.2f}',
                'pH Condition': ph_condition
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
