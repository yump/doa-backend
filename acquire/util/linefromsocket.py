import socket

def linefromsocket(sock, bufsz=1024):
	result = bytes()
	char = sock.recv(1)
	result += char
	while char != b'\n' and len(result) < bufsz:
		char = sock.recv(1)
		result += char
	return result

			
		
