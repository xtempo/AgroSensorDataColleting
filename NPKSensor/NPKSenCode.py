import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Open bus 0, device 0
spi.max_speed_hz = 1350000

def read_channel(channel):
    # Read SPI data from the MCP3008 chip
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def main():
    try:
        while True:
            # Read NPK values (assuming you connect NPK sensor to channel 0)
            npk_value = read_channel(0)

            # Print the raw NPK sensor value
            print(f'NPK Sensor Value: {npk_value}')

            # Add your conversion logic here if necessary
            # For example, map the value to N, P, K levels
            # e.g., npk_nitrogen = npk_value * conversion_factor

            time.sleep(1)

    except KeyboardInterrupt:
        print("Program stopped")

    finally:
        spi.close()

if __name__ == "__main__":
    main()
