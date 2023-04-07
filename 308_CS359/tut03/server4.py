import socket
import select
import sys

HOST = sys.argv[1]  # Get host from command line argument
PORT = int(sys.argv[2])  # Get port from command line argument

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow reuse of socket address
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to a specific address and port
try:
    server_socket.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

# Listen for incoming connections
server_socket.listen(10)

# List of sockets for select() call
sockets_list = [server_socket]

print(f'Server started on port {PORT}')

# Loop indefinitely to handle incoming connections
while True:
    # Use select to multiplex between sockets
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    # Handle sockets with incoming data
    for socket in read_sockets:
        # New connection
        if socket == server_socket:
            client_socket, address = server_socket.accept()
            print(f'Connected with client socket number {client_socket.fileno()}')
            sockets_list.append(client_socket)
        # Data from client
        else:
            data = socket.recv(1024)
            if data:
# Echo data back to client
                print(f'Client socket {socket.fileno()} sent message: {data.decode().strip()}')
                print(f'Sending reply: {data.decode().strip()}')
                socket.send(data)
            # Client disconnected
            else:
                print(f'Connection closed from {socket.getpeername()}')
                sockets_list.remove(socket)
                socket.close()

    # Handle exceptional conditions
    for socket in exception_sockets:
        print(f'Exceptional condition on {socket.getpeername()}')
        sockets_list.remove(socket)
        socket.close()
