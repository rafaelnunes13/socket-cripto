import socket
import random
from simplecrypt import encrypt, decrypt

host = ""
port = 7000

recebe = ""

addr = (host, port)

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.bind(addr)
serv_socket.listen(10) #limite de conexoes

print "Aguardando conexao..."

con, cliente = serv_socket.accept()

print 'Conectado'
print 'Aguardando uma mensagem'

recebe = con.recv(1024)
if recebe:

	bitsChave = 128
	chaveMax = (2**bitsChave)-1

	b = random.randrange(1, chaveMax)

	data = eval(recebe)

	p = data[0]
	g = data[1]
	A = data[2]

	B = pow(g, b, p)

	con.send(str(B))

	kb = pow(A, b, p)

	recebe = con.recv(1024)
	if recebe:
		print "Mensagem recebida: " + recebe
		print "Descriptografando..."
		msgDec = decrypt(str(kb), recebe)
		
		print "Mensagem descriptografada: " + msgDec
	
serv_socket.close()