import socket
from utils import hash_function

host = '127.0.0.1'
port = 9899
size = 1024

secret = 'cran'

cc = 'client-challenge'
cr = ''
sc = ''

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))

# client asking the server for authentication
sock.send('AUTH')

# client verifies the expected value of 'sr'
def check_sr(sr, sc):
	return sr == hash_function(sc + cc + secret)

while True:
	data = sock.recv(size)

	# server challenge in responce to the 'AUTH' request
	if 'SC.' in data:
		sc = data[3:]
		cr = hash_function(cc + sc + secret)

		# client sends 'cr' and 'cc' to the server
		sock.send('CR.' + cr + 'CC.' + cc)

	# server sends 'sr'
	if 'SR.' in data:
		sr = data[3:]

		if check_sr(sr, sc):
			print 'TRUE'
		else:
			print 'FALSE'

	# client receive an error response
	if 'ERROR' in data:
		print 'CLIENT ERROR'
		break

sock.close()
