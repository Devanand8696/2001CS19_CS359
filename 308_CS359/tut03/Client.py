import socket
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <ip_address> <port_number>")
        sys.exit(1)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print("Connected to server")
    except ConnectionRefusedError:
        print(f"Failed to connect to server {HOST}:{PORT}")
        sys.exit(1)
    except OSError:
        print("Server is currently connected to another client. Please wait.")
        sys.exit(1)

    while True:
        message = input("Please enter the message to the server: ")
        s.sendall(message.encode())
        data = s.recv(1024)
        print(f"Server replied: {data.decode()}")
        response = input("Do you wish to continue? Y/N ")
        if response.lower() != "y":
            break

    s.close()
