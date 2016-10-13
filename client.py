import random
from simplecrypt import encrypt, decrypt
import socket
import time

#Funcao para encontrar numero primo aleatorio dentro de um range
def randomPrimo(ini, fim):
	nrPrimo = random.randrange(ini, fim)
	ehPrimo = 0
	contPrimo = 0

	while ehPrimo == 0:
		i = 1
		while i < 6:
			i += 1
			if ((i**(nrPrimo-1)) % nrPrimo) == 1:
				contPrimo += 1
			else:
				i = 6

		if contPrimo == 5:
			ehPrimo = 1
		else:
			ehPrimo = 0
			contPrimo = 0
			nrPrimo = random.randrange(ini, fim)

	#print "%d ? %d" % (nrPrimo, ehPrimo)

	return nrPrimo

ip = "127.0.0.1"
port1 = 7000
port2 = 7001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = ((ip, port1))

count = 0

while count < 10:

	if count > 4:
		addr = ((ip, port2))

	print "Tentando conectar a" + str(addr)

	try:
	    client_socket.connect(addr)
	    break
	except socket.error as msg:	    
	    count = count + 1
	    time.sleep(5)
	    continue

if count == 10:
	print "Servico indisponivel. Tente mais tarde"
else:

	p = randomPrimo(2, 2048)
	g = randomPrimo(1, p-1)

	bitsChave = 128

	chaveMax = (2**bitsChave)-1

	a = random.randrange(1, chaveMax)

	A = pow(g, a, p)

	data = [p, g, A]

	data = str(data)

	client_socket.send(data)

	B = int(client_socket.recv(1024))

	ka = pow(B, a, p)

	msg = raw_input("Digite a mensagem para enviar para 'B': ")

	msgEnc = encrypt(str(ka), msg)

	print "Mensgem criptografada: " + msgEnc
	print "Mensagem original: " + msg

	client_socket.send(msgEnc)

client_socket.close()

#msg = raw_input("Digite a mensagem para enviar para 'B': ")

#msgEnc = encrypt(str(ka), msg)