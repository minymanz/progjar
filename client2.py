import sys
import socket
import threading

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 5001)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
name = raw_input("nama : ")
sock.sendall(name)

print >>sys.stderr, 'User online : '
n = int(sock.recv(4))
for i in xrange(0,n-1):
    name = sock.recv(256)
    print >>sys.stderr, '- %s' % name
#id1 = sock.recv(256)
#id2 = sock.recv(256)
#print >>sys.stderr, '%s, %s is online' % (id1,id2)

def send():
    while True :
        message = raw_input()
        #print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(name)
        sock.sendall(message)
        

def receive():
    while True :
        nama = sock.recv(256)
        status = sock.recv(256)
        data = sock.recv(256)
        print >>sys.stderr, '%s (%s) : %s' % (nama,status,data)


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
