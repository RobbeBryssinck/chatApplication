import socket
import sys
import os
import optparse
from threading import *

screenLock = Semaphore(value=5)
global logs

def createServer(port):

	# create a TCP socket
	sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# bind the socket to the port
	server_address = ('localhost', port)
	print("starting up on {} port {}".format(*server_address))
	sck.bind(server_address)

	# put the socket into server mode
	sck.listen(5)

	return sck


def runServer(sck, conn, client, logs):

	
	data = conn.recv(1024)
	message = client[0] + ': ' + data.decode() + '\n'
	print(message)
	logs.write(message)

	conn.close()


def main():

	# option to set port when launching the server
	parser = optparse.OptionParser("Usage: pyhon3 server.py -p <server port>")
	parser.add_option('-p', dest='port', type='int', help="specify target port")
	(options, args) = parser.parse_args()
	port = options.port
	
	if port == None:
		print(parser.usage)
		exit(0)

	# create server logs
	if not os.path.exists('./logs.txt'):
		os.mknod('./logs.txt')
	logs = open('./logs.txt', 'w')

	# create the socket
	sck = createServer(port)

	# run the server
	while True:

		# wait for connection and start thread
		conn, client = sck.accept()
		t = Thread(target=runServer, args=(sck, conn, client, logs))
		t.start()


if __name__ == '__main__':
	main()
