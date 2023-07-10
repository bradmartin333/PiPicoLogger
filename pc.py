# This program gets all USB devices connected to the PC in a list
# and connects to the Pi Pico. It then sends a message to the Pico
# and waits for a response. The response is appended to a file
# called "data.txt"

import serial
import serial.tools.list_ports
import time

# Get a list of all USB devices connected to the PC
ports = serial.tools.list_ports.comports()
pico_port = None
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))
    if 'PID=239A' in hwid:
        print("Found Pico on port: ", port)
        pico_port = port

# If no Pico found, exit
if pico_port is None:
    print("No Pico found")
    exit()

# Connect to the Pico
s = serial.Serial(port=pico_port, parity=serial.PARITY_EVEN,
                  stopbits=serial.STOPBITS_ONE, timeout=1)

# Flush the serial buffer
s.flush()

while True:
    # Send a message to the Pico
    s.write("data\n".encode())
    # Read the response from the Pico
    mes = s.read_until()
    # Decode the response and remove newline
    response = mes.decode().strip()
    # Remove boot string
    response = response.split('\\')[-1]
    # Print the response
    print(response)
    # Write the response to a file
    with open("data.txt", "a") as f:
        f.write(response + '\n')
    # Wait 1 second
    time.sleep(1)
