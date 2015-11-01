import socket
from utils import hash_function

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = '127.0.0.1'
port = 9899
size = 1024

secret = 'cram'

sc = 'server-challenge'

sock.bind((host, port))
sock.listen(1)
print "CRAM server listening on port {0}".format(port)

# server verifies the expected value of 'cr'
def check_cr(cr, cc):
	return cr == hash_function(cc + sc + secret)

# server daemon
while True:
	connection, client = sock.accept()

	try:
		while True:
			data = connection.recv(1024)

			print data, len(data)

			if data == 'AUTH':
				connection.send('SC.' + sc)

			if 'CR.' in data:
				try:
					cc_index = data.index('CC.')
				except (ValueError):
					connection.send('ERROR')
					break

				cr = data[3:cc_index]
				cc = data[(cc_index+3):]

				# server verified 'cr'
				if check_cr(cr, cc):
					sr = hash_function(sc + cc + secret)
					connection.send('SR.' + sr)
				else:
					connection.send('ERROR')
					break

	finally:
		connection.close()
