import socket
import sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a public host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections (backlog argument specifies the maximum number of queued connections)
server_socket.listen(1)

while True:
    # Wait for a connection
    print('Waiting for a connection...')
    client_socket, address = server_socket.accept()
    print(f'Connected with client socket number {client_socket.fileno()}')

    # Handle the client request
    while True:
        try:
            # Receive the message from the client
            message = client_socket.recv(1024).decode()

            # Check if the message is empty, then terminate the connection
            if not message:
                break

            # Evaluate the arithmetic expression
            try:
                result = str(eval(message))
                # Send the result back to the client
                print(f'Client socket {client_socket.fileno()} sent message: {message}')
                print(f'Sending reply: {result}')
                client_socket.sendall(result.encode())
            except:
                # Send an error message back to the client if the input is invalid
                error_message = "Invalid input, please enter a valid arithmetic expression."
                client_socket.sendall(error_message.encode())
        except:
            # If there's an error, terminate the connection
            client_socket.close()
            break

    print(f'Client socket {client_socket.fileno()} disconnected')
    client_socket.close()

# Close the server socket
server_socket.close()
