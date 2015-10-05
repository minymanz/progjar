import sys
import socket
import threading

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Bind the socket to the port
server_address = ('localhost', 10000)
server_address2 = ('localhost', 5000)
server_address3 = ('localhost', 6000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
print >>sys.stderr, 'starting up on %s port %s' % server_address2
print >>sys.stderr, 'starting up on %s port %s' % server_address3
sock.bind(server_address)
sock2.bind(server_address2)
sock3.bind(server_address3)

# Listen for incoming connections
sock.listen(1)
sock2.listen(1)
sock3.listen(1)

print >>sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()
connection2, client_address2 = sock2.accept()
connection3, client_address3 = sock3.accept()
print >>sys.stderr, 'connection from', client_address
print >>sys.stderr, 'connection from', client_address2
print >>sys.stderr, 'connection from', client_address3


def client1():
    while True :
        name = connection.recv(256)
        data = connection.recv(256)
        print >>sys.stderr, 'received "%s"' % data
        print >>sys.stderr, 'sending data back to the client'
        connection2.sendall(name)
        connection2.sendall(data)
        connection3.sendall(name)
        connection3.sendall(data)
        

def client2():
    while True :
        name2 = connection2.recv(256)
        data2 = connection2.recv(256)
        print >>sys.stderr, 'received "%s"' % data2
        print >>sys.stderr, 'sending data back to the client'
        connection.sendall(name2)
        connection.sendall(data2)
        connection3.sendall(name2)
        connection3.sendall(data2)


def client3():
    while True :
        name3 = connection3.recv(256)
        data3 = connection3.recv(256)
        print >>sys.stderr, 'received "%s"' % data3
        print >>sys.stderr, 'sending data back to the client'
        connection.sendall(name3)
        connection.sendall(data3)
        connection2.sendall(name3)
        connection2.sendall(data3)


threads = []

t=threading.Thread(target=client1)
tt=threading.Thread(target=client2)
ttt=threading.Thread(target=client3)

threads.append(t)
threads.append(tt)
threads.append(ttt)

t.start()
tt.start()
ttt.start()

for t in threads:
    t.join()