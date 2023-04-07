import socket
import threading
import sys

def handle_client(conn, addr):
    print(f"Connected with client socket number {addr[1]}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print(f"Client socket {addr[1]} disconnected")
                break
            message = data.decode().strip()
            print(f"Client socket {addr[1]} sent message: {message}")
            try:
                result = eval(message)
                conn.send(str(result).encode())
                print(f"Sending reply: {result}")
            except:
                conn.send("Invalid input".encode())
                print("Sending reply: Invalid input")
        except:
            print(f"Error with client {addr}")
            break
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python server2.py <ip_address> <port_number>")
        sys.exit(1)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server is listening on {HOST}:{PORT}")
    except:
        print(f"Failed to bind socket on {HOST}:{PORT}")
        sys.exit(1)

    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()
