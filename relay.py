#
# Author: Neal Anders <neal.anders@gmail.com>
# Date: 2025-10-26
# License: Whatever?
#
# This script sends commands to a MusRock RS485 Relay Module.
# Reference: https://www.amazon.com/dp/B0FMNXWRVG
#
# It requires the pyserial library to be installed. 
# You can install it using pip: pip install pyserial
# Usage: python relay.py <COM_PORT> <COMMAND_NUMBER>
# Example: python relay.py COM10 1
# Make sure to replace 'COM10' with your actual COM port.
#
# Note: Serial communication is via the RS-485 interface.

import serial
import sys

# These are specific to the MusRock RS485 Relay Board, and assumes a wiring arrangement of 'Normally Open'.
relay_commands = [
    bytes([0xFF, 0x05, 0x00, 0x00, 0xFF, 0x00, 0x99, 0xE4]),  # Engage Relay 1
    bytes([0xFF, 0x05, 0x00, 0x00, 0x00, 0x00, 0xD8, 0x14]),  # Disengage Relay 1
]

# Check if the command line arguments are provided
if len(sys.argv) > 2: # need a com port and relay number/command
    com = sys.argv[1]
    cmd = int(sys.argv[2])
    cmd_num = int(cmd) -1 # Convert to 1-based index from 0-based index)
else: 
    print("Usage: python relay.py <COM_PORT> <COMMAND_NUMBER>")
    print("Example: python relay.py COM10 1")
    sys.exit(1)

# Make sure the command number is valid
if cmd_num < 0 or cmd_num >= len(relay_commands):
    print(f"Invalid command number: {cmd_num + 1}. Must be between 1 and {len(relay_commands)}.")
    sys.exit(1) 

# open the serial port
try:
    conn = serial.Serial(com, 9600, timeout=1)
except serial.SerialException as e:
    print(f"Error opening serial port {com}: {e}")
    sys.exit(1) 

# Write the command to the relay
conn.write(relay_commands[cmd_num])  # Send command
response = conn.read(8)  # Read the response (8 bytes expected)
print(f"Response: {response.hex().upper()}")  # Print the response in hex format