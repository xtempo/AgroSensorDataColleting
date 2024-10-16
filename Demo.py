import time
import board
import adafruit_dht
import csv
from datetime import datetime
import digitalio
import random  # For simulating values

class SensorApp:
    def __init__(self):
        # Define the pins where the sensors are connected
        self.DHT_PIN = board.D4  # DHT sensor pin
        self.SOIL_MOISTURE_PIN = board.D17  # Soil moisture sensor pin
        self.SMOKE_SENSOR_PIN = board.D18  # Smoke sensor pin
        self.PH_SENSOR_PIN = board.D12  # Digital pH sensor pin

        # Create instances for the sensors
        self.dht_sensor = adafruit_dht.DHT11(self.DHT_PIN)
        self.smoke_sensor = digitalio.DigitalInOut(self.SMOKE_SENSOR_PIN)
        self.smoke_sensor.direction = digitalio.Direction.INPUT
        self.soil_moisture_sensor = digitalio.DigitalInOut(self.SOIL_MOISTURE_PIN)
        self.soil_moisture_sensor.direction = digitalio.Direction.INPUT
        self.ph_sensor = digitalio.DigitalInOut(self.PH_SENSOR_PIN)
        self.ph_sensor.direction = digitalio.Direction.INPUT

        # Set up the CSV file
        self.csvfile = open('sensorData.csv', mode='w', newline='')
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.get_fieldnames())
        self.writer.writeheader()

        # Initialize max and min values
        self.max_temperature = float('-inf')
        self.min_temperature = float('inf')
        self.max_humidity = float('-inf')
        self.min_humidity = float('inf')

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
            'Benzene Concentration (ppm)', 
            'Alcohol Concentration (ppm)',
            'Ammonia Concentration (ppm)',
            'CO2 Concentration (ppm)',
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
            return None, None

    def read_soil_moisture(self):
        return self.soil_moisture_sensor.value  # Returns True (wet) or False (dry)

    def read_smoke_sensor(self):
        return self.smoke_sensor.value  # Returns True (smoke detected) or False (no smoke)

    def read_pkn(self):
        # Simulated PKN value for demonstration
        return random.uniform(0, 100)

    def read_gas_concentrations(self):
        # Simulate gas concentrations for demonstration
        benzene_concentration = random.uniform(0, 100)
        alcohol_concentration = random.uniform(0, 100)
        ammonia_concentration = random.uniform(0, 100)
        co2_concentration = random.uniform(0, 100)

        return benzene_concentration, alcohol_concentration, ammonia_concentration, co2_concentration

    def read_ph_sensor(self):
        # Simulate pH reading (replace with actual sensor logic)
        return random.uniform(0, 14)  # pH scale typically ranges from 0 to 14

    def get_ph_condition(self, ph_value):
        if ph_value < 5.5:
            return "More Acidic"
        elif 5.5 <= ph_value < 7:
            return "Less Acidic"
        elif ph_value == 7:
            return "Neutral"
        elif 7 < ph_value <= 8.5:
            return "Less Basic"
        else:
            return "More Basic"

    def log_data(self):
        while True:
            current_time = datetime.now()
            print(f"Current time: {current_time.isoformat()}", flush=True)

            temperature, humidity = self.read_dht_sensor()
            pkn = self.read_pkn()
            soil_moisture = self.read_soil_moisture()
            soil_moisture_percentage = 100 if soil_moisture else 0
            smoke_detected = self.read_smoke_sensor()
            benzene, alcohol, ammonia, co2 = self.read_gas_concentrations()
            ph_value = self.read_ph_sensor()
            ph_condition = self.get_ph_condition(ph_value)

            # Update max and min values
            if temperature is not None:
                if temperature > self.max_temperature:
                    self.max_temperature = temperature
                if temperature < self.min_temperature:
                    self.min_temperature = temperature
            
            if humidity is not None:
                if humidity > self.max_humidity:
                    self.max_humidity = humidity
                if humidity < self.min_humidity:
                    self.min_humidity = humidity

            # Print the data to the console
            print(f'Temperature: {temperature}°C  Humidity: {humidity}%  PKN: {pkn}  '
                  f'Soil Moisture: {soil_moisture_percentage:.2f}%  Smoke Detected: {"Yes" if smoke_detected else "No"}', flush=True)
            print(f'Gas Concentrations - Benzene: {benzene:.2f} ppm, Alcohol: {alcohol:.2f} ppm, '
                  f'Ammonia: {ammonia:.2f} ppm, CO2: {co2:.2f} ppm', flush=True)
            print(f'pH Level: {ph_value:.2f}  pH Condition: {ph_condition}', flush=True)

            # Get the current timestamp
            timestamp = current_time.isoformat()

            # Write the data to the CSV file
            self.writer.writerow({
                'Timestamp': timestamp,
                'Temperature (°C)': f'{temperature}' if temperature is not None else 'N/A',
                'Humidity (%)': f'{humidity}' if humidity is not None else 'N/A',
                'Max Temperature (°C)': f'{self.max_temperature:.2f}',
                'Min Temperature (°C)': f'{self.min_temperature:.2f}',
                'PKN (units)': f'{pkn}',
                'Soil Moisture (%)': f'{soil_moisture_percentage:.2f}',
                'Smoke Detected': 'Yes' if smoke_detected else 'No',
                'Benzene Concentration (ppm)': f'{benzene:.2f}',
                'Alcohol Concentration (ppm)': f'{alcohol:.2f}',
                'Ammonia Concentration (ppm)': f'{ammonia:.2f}',
                'CO2 Concentration (ppm)': f'{co2:.2f}',
                'pH Level': f'{ph_value:.2f}',
                'pH Condition': ph_condition
            })
            # Write an empty row for better visualization
            self.writer.writerow({})  # Adds an empty row

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
