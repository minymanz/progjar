import sys
import socket
import threading
import re

sock = []


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

id1=connection.recv(256)
id2=connection2.recv(256)
id3=connection3.recv(256)

print >>sys.stderr, '%s connected' % id1
print >>sys.stderr, '%s connected' % id2
print >>sys.stderr, '%s connected' % id3

connection.sendall(id2)
connection.sendall(id3)
connection2.sendall(id1)
connection2.sendall(id3)
connection3.sendall(id1)
connection3.sendall(id2)

def client1():
    while True :
        name = connection.recv(256)
        data = connection.recv(256)
        print >>sys.stderr, 'received "%s"' % data
        print >>sys.stderr, 'sending data back to the client'
        count1 = len(re.findall(r'\w+', data))

        if count1 == 1 :
            iden = 'server'
            data = 'server'
        else :
            iden = data.split(' ',1)[0]
            sent = data.split(' ',1)[1]

        if iden == id2 :
            connection2.sendall(name)
            connection2.sendall('private')
            connection2.sendall(sent)
        elif iden == id3 :
            connection3.sendall(name)
            connection3.sendall('private')
            connection3.sendall(sent)
        elif iden == "all" :
            connection2.sendall(name)
            connection2.sendall('group')
            connection2.sendall(sent)
            connection3.sendall(name)
            connection3.sendall('group')
            connection3.sendall(sent)
        elif iden == 'server' or sent == 'server' :
            connection.sendall('server')
            connection.sendall('alert')
            connection.sendall('User not found or Syntax error')
        else :
            connection.sendall('server')
            connection.sendall('alert')
            connection.sendall('User not found or Syntax error')
        

def client2():
    while True :
        name2 = connection2.recv(256)
        data2 = connection2.recv(256)
        print >>sys.stderr, 'received "%s"' % data2
        print >>sys.stderr, 'sending data back to the client'
        count2 = len(re.findall(r'\w+', data2))

        if count2 == 1 :
            iden2 = 'server'
            data2 = 'server'
        else :
            iden2 = data2.split(' ',1)[0]
            sent2 = data2.split(' ',1)[1]

        if iden2 == id1 :
            connection.sendall(name2)
            connection.sendall('private')
            connection.sendall(sent2)
        elif iden2 == id3 :
            connection3.sendall(name2)
            connection3.sendall('private')
            connection3.sendall(sent2)
        elif iden2 == "all" :
            connection.sendall(name2)
            connection.sendall('group')
            connection.sendall(sent2)
            connection3.sendall(name2)
            connection3.sendall('group')
            connection3.sendall(sent2)
        elif iden2 == 'server' or sent2 == 'server' :
            connection2.sendall('server')
            connection2.sendall('alert')
            connection2.sendall('User not found or Syntax error')
        else :
            connection2.sendall('server')
            connection2.sendall('alert')
            connection2.sendall('User not found or Syntax error')


def client3():
    while True :
        name3 = connection3.recv(256)
        data3 = connection3.recv(256)
        print >>sys.stderr, 'received "%s"' % data3
        print >>sys.stderr, 'sending data back to the client'
        count3 = len(re.findall(r'\w+', data3))

        if count3 == 1 :
            iden3 = 'server'
            data3 = 'server'
        else :
            iden3 = data3.split(' ',1)[0]
            sent3 = data3.split(' ',1)[1]

        if iden3 == id1 :
            connection.sendall(name3)
            connection.sendall('private')
            connection.sendall(sent3)
        elif iden3 == id2 :
            connection2.sendall(name3)
            connection2.sendall('private')
            connection2.sendall(sent3)
        elif iden3 == "all" :
            connection.sendall(name3)
            connection.sendall('group')
            connection.sendall(sent3)
            connection2.sendall(name3)
            connection2.sendall('group')
            connection2.sendall(sent3)
        elif iden3 == 'server' or sent3 == 'server' :
            connection3.sendall('server')
            connection3.sendall('alert')
            connection3.sendall('User not found or Syntax error')
        else :
            connection3.sendall('server')
            connection3.sendall('alert')
            connection3.sendall('User not found or Syntax error')


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