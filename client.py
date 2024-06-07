import os
import sys
import socket
import time
import getpass
import json

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port to connect to
host = 'localhost'
port = 8069

while True:
    try:
        # Attempt to connect to the server
        print(f"Trying to connect to {host} on port {port}")
        s.connect((host, port))
        print(f"Successfully connected to {host} on port {port}")
        
        # Send the event name and JSON data
        s.send(("initialization|"+json.dumps({"username": getpass.getuser()})).encode())  # Convert the string to bytes
        
        while True:
            try:
                # Receive data from the server
                received_data = s.recv(1024)
                if received_data:
                    print(f"Received command: {received_data.decode()}")
                    # Split the received data into event name and JSON payload
                    event_name, json_payload = received_data.decode().split('|', 1)
                    print(f"Event Name: {event_name}, Payload: {json_payload}")
                    # Deserialize the JSON payload
                    command = json.loads(json_payload)
                    print(f"Main command: {command}")
                    
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

