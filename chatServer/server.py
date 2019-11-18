import socket
import sys
import os
import optparse
from threading import *


def createServer(ip, port):

	# create a TCP socket
	sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# bind the socket to the port
	server_address = (ip, port)
	print("starting up on {} port {}".format(*server_address))
	sck.bind(server_address)

	# put the socket into server mode
	sck.listen(5)

	return sck


def clientHandler(sck, conn, client, logs):

	# initialise user
	name = conn.recv(2014)

	# receive data
	while True:
		try:
			data = conn.recv(1024)
			message = name.decode() + ': ' + data.decode() + '\n'
			print(message)
			updateClients(message)
			logs.write(message)
		except:
			message = name.decode() + " closed the connection.\n"
			logs.write(message)
			print(message)
			break

	conn.close()


def updateClients(message):
	for client in clients:
		client.send(bytes(message, 'ASCII'))


def main():

	# option to set port when launching the server
	parser = optparse.OptionParser("Usage: python3 server.py -h <server ip> -p <server port>")
	parser.add_option('-p', dest='port', type='int', help="specify server port")
	parser.add_option('-h', dest='ip', type='string', help="specify server ip")
	(options, args) = parser.parse_args()
	port = options.port
	ip = options.ip
	
	if port == None:
		print(parser.usage)
		exit(0)

	logs = open('./logs.txt', 'a+')
	sck = createServer(ip, port)
	

	while True:

		# wait for connection
		conn, client = sck.accept()

		clients.append(conn)

		# log connection
		message = client[0] + " connected.\n"
		print(message)
		logs.write(message)
		
		# start thread
		t = Thread(target=clientHandler, args=(sck, conn, client, logs))
		t.start()

clients = []

if __name__ == '__main__':
	main()
