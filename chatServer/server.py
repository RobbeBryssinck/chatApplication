import socket
import sys

# Create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print("starting up on {} port {}".format(*server_address))
s.bind(server_address)

while True:
    print("\nWaiting to receive message")
    data, address = s.recvfrom(4096)

    print("Received {} bytes from {}".format(len(data), address))
    print(data)

    if data:
        sent = sock.sendto(data, address)
        print("Sent {} bytes back to {}".format(sent, address))

