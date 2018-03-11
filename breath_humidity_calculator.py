import Adafruit_DHT
import time
import csv
from datetime import datetime



sensor = Adafruit_DHT.DHT22


def get_data(pin_number, volume):
    print(pin_number)

    # Ask the DHT 22 at the given pin number for relative humidity and temperature
    relative_humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_number)
    print('Relative Humidity: {0:.4f}'.format(relative_humidity))
    #print('Temperature: {0:.4f}'.format(temperature))

    # Convert relative humidty and temperature to absolute humidity measured in g of water per m^3
    absolute_humidity = (6.112* 2.71828**((17.67*temperature)/(temperature+243.5)) *relative_humidity *2.1674)/(273.15+temperature)
    #print('Absolute Humidity: {0:.4f}'.format(absolute_humidity))

    # Calculate water in breath by multiplying average breath volume by absolute humidity
    g_water = volume * absolute_humidity
    #print("Kg Water: {0:.8f}".format(g_water))
    
    data = {
        'temperature': temperature,
        'relative_humidity': relative_humidity,
        'absolute_humidity': absolute_humidity,
        'g_water': g_water
    }
    return data

now = datetime.now()
run_name = raw_input("What is the name of this run? ")
print(run_name)
filename = '/home/pi/humidity_data/{}_{:%Y-%m-%d_%H-%M-%S}.csv'.format(run_name, now)

volume = raw_input("What is the tidal volume in m^3? ")

with open(filename, 'w', 0) as csvfile:
    fieldnames = ['time',
        'input_absolute_humidity',
        'input_temperature',
        'input_relative_humidity',
        'input_g_water',
        'output_absolute_humidity',
        'output_temperature',
        'output_relative_humidity',
        'output_g_water',
        'water_lost',
        'breathing_rate',
        'water_lost_per_minute']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)

    while True:
        breathing_rate_string = input("What is your breathing rate?")
        breathing_rate = float(breathing_rate_string)
        incoming_data = get_data(17, volume)
        outgoing_data = get_data(4, volume)
        water_lost =  outgoing_data['g_water'] - incoming_data['g_water']
        water_lost_per_minute = water_lost * breathing_rate
        print("Water Lost Per Minute: {0:.8f}".format(water_lost_per_minute))
        print("Water Lost: {0:.8f}".format(water_lost))
        current_time = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.now())
        writer.writerow([
            current_time,
            incoming_data['absolute_humidity'],
            incoming_data['temperature'],
            incoming_data['relative_humidity'],
            incoming_data['g_water'],
            outgoing_data['absolute_humidity'],
            outgoing_data['temperature'],
            outgoing_data['relative_humidity'],
            outgoing_data['g_water'],
            water_lost,
            breathing_rate,
            water_lost_per_minute
        ])

