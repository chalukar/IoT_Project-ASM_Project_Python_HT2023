import time
import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import subprocess
import schedule
import random

from decimal import Decimal

# Imports for sensor
import board
import busio

import adafruit_tsl2591 # High range lux sensor

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)

sensor = adafruit_tsl2591.TSL2591(i2c) # High range lux sensor

broker_address = "test.mosquitto.org"
port = 1883
topic_to_subscribe = "iotproject/asmvacationmode_subscribe"
topic_to_publish = "iotproject/asmvacationmode_publish"
received_message =None
dateformat_str = "%m-%d-%Y"
current_date = datetime.datetime.now().strftime("%m-%d-%Y")

lux_min_threshold = 0.900
lux_max_threshold = 8.000
device_id = '4' # device ID of your light

def on_message(client, userdata, message):
    global received_message
    received_message = str(message.payload.decode("utf-8"))

def vacationMode():
    global received_message
    lux = sensor.lux
    lux_value = round(Decimal(lux), 3) # Rounds the lux value to 3 decimals, and prints it
    print(f"Received message: {received_message}")
    print('Lux: {0} lux'.format(lux_value))
    print(current_date)
    if received_message is not None:
        result_list = received_message.split(',')
        start_date_str = result_list[0]
        formatted_date = datetime.datetime.strptime(start_date_str, dateformat_str).date()
        start_date = formatted_date.strftime("%m-%d-%Y")
        end_date_str = result_list[1]
        formatted_date = datetime.datetime.strptime(end_date_str, dateformat_str).date()
        end_date = formatted_date.strftime("%m-%d-%Y")
        print(f"Start Date: {start_date}")
        print(f"End Date: {end_date}")
        if start_date <= current_date <= end_date:
            if lux_value < lux_max_threshold:
                schedule.run_pending()
                return run_schedule()
             
    else:
        result ="Vacation mode not activated"
        print(result)
        return result
    
def get_random_int():
    random_delay = random.randint(1, 10)  # Random delay in minutes
    print(random_delay)
    if random_delay == 1: 
        return turn_on_lights()
    return "Light not turned on"


def turn_on_lights():
    light_status = "Lights turned on"
    print(light_status)
    subprocess.run(["tdtool", "--on", "4"])
    schedule.every(2).minutes.do(turn_off_lights).tag('turn_off_job')
    return light_status

def turn_off_lights():
    subprocess.run(["tdtool", "--off", "4"])
    schedule.clear('turn_off_job')
    light_status = "Lights turned off"
    print(light_status)
    return light_status

def run_schedule():
    schedule.every(3).minutes.do(get_random_int).tag('lights_job')
    return get_random_int()

# Start the schedule
run_schedule()

# Create MQTT client
client = mqtt.Client()

# Set callback function for message reception
client.on_message = on_message
# Connect to the broker
client.connect(broker_address, port, 60)

# Subscribe to the topic
client.subscribe(topic_to_subscribe)

# Loop to receive messages
client.loop_start()

try:
    while True:
        # Your main program logic can be placed here
        client.publish(topic_to_publish, str(vacationMode()))
        # Wait for some time
        time.sleep(1)

except KeyboardInterrupt:
    schedule.clear('lights_job')
    print("Program terminated by user")