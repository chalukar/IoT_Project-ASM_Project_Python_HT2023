
# ---- light On --------------
import subprocess
command = ['tdtool', '--on', '4']
# Run the command
process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Get the standard output and error
output = process.stdout
error = process.stderr

# Check if the command was executed successfully
if process.returncode == 0:
    print('Command executed successfully')
    print('Output:', output)
else:
    print('An error occurred while executing the command')
    print('Error:', error)


#----- light Off-------------------
import subprocess
command = ['tdtool', '--off', '4']

# Run the command
process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Get the standard output and error
output = process.stdout
error = process.stderr

# Check if the command was executed successfully
if process.returncode == 0:
    print('Command executed successfully')
    print('Output:', output)
else:
    print('An error occurred while executing the command')
    print('Error:', error)


#----- brightness-------------------
import subprocess

def set_light_brightness(device_id, brightness):
    try:
        # Run the tdtool command to set brightness
        subprocess.run(["tdtool", "--dimlevel", str(brightness), "--dim", str(device_id)])
        print(f"Light brightness set to {brightness}% for device {device_id}")
    except subprocess.CalledProcessError as e:
        print(f"Error setting light brightness: {e}")

# Replace 'your_device_id' with the actual device ID of your light
device_id = '4'

# Set the desired brightness level (0-100)
brightness_level = 50

# Call the function to set light brightness
set_light_brightness(device_id, brightness_level)

#----------------------------
import subprocess
import time

def turn_on_light(device_id):
    subprocess.run(["tdtool", "--on", str(device_id)])

def turn_off_light(device_id):
    subprocess.run(["tdtool", "--off", str(device_id)])

def set_light_brightness(device_id, brightness):
    result = subprocess.run(["tdtool", "--dimlevel", str(brightness), "--dim", str(device_id)], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    print(f"Light brightness set to {brightness}% for device {device_id}")
    # subprocess.run(["tdtool", "--dimlevel", str(brightness), "--dim", str(device_id)])

# Replace with the actual device ID of your light
light_device_id = 4

try:
    # Turn on the light
    turn_on_light(light_device_id)
    time.sleep(2)  # Optional: Wait for 2 seconds before changing brightness

    # Set brightness to 50% (adjust as needed)
    set_light_brightness(light_device_id, 50)

    # Optional: Wait for a while before turning off the light
    time.sleep(5)

    # Turn off the light
    turn_off_light(light_device_id)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    print("Script completed.")



