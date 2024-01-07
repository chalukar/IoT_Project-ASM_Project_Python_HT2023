# Imports for MQTT
import time
import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import subprocess

from decimal import Decimal

# Imports for sensor
import board
import busio

import adafruit_tsl2591 # High range lux sensor

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)

# Uncomment your current sensor :)
sensor = adafruit_tsl2591.TSL2591(i2c) # High range lux sensor

# Set MQTT broker and topic
broker = "test.mosquitto.org"	# Broker 

pub_topic = "iotproject/asmnaturallightlux" # asm -scensmanagement  send messages to this topic

lux_min_threshold = 0.900
lux_max_threshold = 8.000
# device ID of your light
device_id = '4'


############### MQTT section ##################

# when connecting to mqtt do this;
def on_connect(client, userdata, flags, rc):
	if rc==0:
		print("Connection established. Code: "+str(rc))
	else:
		print("Connection failed. Code: " + str(rc))
		
def on_publish(client, userdata, mid):
    print("Published: " + str(mid))
	
def on_disconnect(client, userdata, rc):
	if rc != 0:
		print ("Unexpected disonnection. Code: ", str(rc))
	else:
		print("Disconnected. Code: " + str(rc))
	
def on_log(client, userdata, level, buf):		# Message is in buf
    print("MQTT Log: " + str(buf))

############### Sensor section ##################	
def is_time_in_range(start_time, end_time, current_time_str):
    current_time = datetime.datetime.strptime(current_time_str, "%H:%M").time()
    start_datetime = datetime.datetime.combine(datetime.datetime.today(), start_time)
    end_datetime = datetime.datetime.combine(datetime.datetime.today(), end_time)
    return start_datetime.time() <= current_time <= end_datetime.time()

def get_time_of_day():
    current_time = datetime.datetime.now().strftime("%H:%M")
    lux = sensor.lux
    lux_value = round(Decimal(lux), 3)  # Rounds the lux value to 3 decimals, and prints it
    if is_time_in_range(datetime.time(00, 0), datetime.time(5, 59), current_time):
        if lux_value < lux_max_threshold:
            turn_on_light(device_id)
            light_status ="Light turned On"
            timeofday_status ="Early Morning."
            outsite_natural_status ="Outdoor Low-level lighting"
            return [light_status,timeofday_status,outsite_natural_status]
        else:
            turn_off_light(device_id)
            light_status ="Light turned Off"
            timeofday_status ="Early Morning."
            outsite_natural_status ="Outdoor Normal lighting"
            return [light_status,timeofday_status,outsite_natural_status]
    elif is_time_in_range(datetime.time(6, 0), datetime.time(11, 59), current_time):
        if lux_value < lux_max_threshold:
            turn_on_light(device_id)
            light_status ="Light turned On"
            timeofday_status ="Good Morning."
            outsite_natural_status ="Outdoor Low-level lighting"
            return [light_status,timeofday_status,outsite_natural_status]
        else:
            turn_off_light(device_id)
            light_status ="Light turned Off"
            timeofday_status ="Good Morning"
            outsite_natural_status ="Outdoor High-level lighting"
            return [light_status,timeofday_status,outsite_natural_status]
    elif is_time_in_range(datetime.time(00, 0), datetime.time(14, 59), current_time):
        if lux_value < lux_max_threshold:
            turn_on_light(device_id)
            light_status ="Light turned On"
            timeofday_status ="Good Afternoon!"
            outsite_natural_status ="Outdoor Low-level lighting"
            return [light_status,timeofday_status,outsite_natural_status]
        else:
            turn_off_light(device_id)
            light_status ="Light turned Off"
            timeofday_status ="Good Afternoon!"
            outsite_natural_status ="Outdoor Normal lighting"
            return [light_status,timeofday_status,outsite_natural_status]
    elif is_time_in_range(datetime.time(15, 0), datetime.time(20, 59), current_time):
        if lux_value < lux_max_threshold:
            turn_on_light(device_id)
            light_status ="Light turned On"
            timeofday_status ="Good Evening!"
            outsite_natural_status ="Outdoor Low-level lighting"
            print(light_status)
            print(timeofday_status)
            print(outsite_natural_status)
            print('Lux: {0} lux'.format(lux_value))
            return [light_status,timeofday_status,outsite_natural_status]
        else:
            turn_off_light(device_id)
            light_status ="Light turned Off"
            timeofday_status ="Good Evening!"
            outsite_natural_status ="Outdoor Normal lighting"
            return [light_status,timeofday_status,outsite_natural_status]
    elif is_time_in_range(datetime.time(21, 0), datetime.time(23, 59), current_time):
        if lux_value < lux_max_threshold:
            turn_on_light(device_id)
            light_status ="Light turned Off"
            timeofday_status ="Good Night!"
            outsite_natural_status ="Outdoor Low-level lighting"
            return [light_status,timeofday_status,outsite_natural_status]
    else:
        turn_off_light(device_id)
        return "UnKnow Time"   
      
def turn_on_light(device_id):
    subprocess.run(["tdtool", "--on", str(device_id)])

def turn_off_light(device_id):
    subprocess.run(["tdtool", "--off", str(device_id)])

		
# Connect functions for MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_log = on_log

# Connect to MQTT 
print("Attempting to connect to broker " + broker)
client.connect(broker)	# Broker address, port and keepalive (maximum period in seconds allowed between communications with the broker)
client.loop_start()


# Loop that publishes message
while True:
	data_to_send = str(get_time_of_day())	# Here, call the correct function from the sensor section depending on sensor
	client.publish(pub_topic, str(data_to_send))
	time.sleep(5.0)	# Set delay