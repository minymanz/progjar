import sys
import socket
import threading

name = raw_input("nama : ")
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 6000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

def send():
    while True :
        message = raw_input()
        #print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(name)
        sock.sendall(message)
        

def receive():
    while True :
        nama = sock.recv(256)
        data = sock.recv(256)
        print >>sys.stderr, '%s : %s' % (nama,data)


threads = []

t=threading.Thread(target=send)
tt=threading.Thread(target=receive)

threads.append(t)
threads.append(tt)

t.start()
tt.start()

for t in threads:
    t.join()

#while True :
#    nama = sock.recv(256)
#    data = sock.recv(256)
#    print >>sys.stderr, '%s : %s' % (nama,data)
#finally:
    #print >>sys.stderr, 'closing socket'
    #sock.close()
