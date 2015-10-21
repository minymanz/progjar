import sys
import socket
import threading
import re

sock = []
server_address = []
connection = [i for i in range(1000)]
client_address = [i for i in range(1000)]
idi = [i for i in range(1000)]
name = [i for i in range(1000)]
data = [i for i in range(1000)]
iden = [i for i in range(1000)]
count = [i for i in range(1000)]
sent = [i for i in range(1000)]
t = [i for i in range(1000)]                    
threads = [i for i in range(1000)]
port = 5000

n = input("Jumlah Client : ")
print >>sys.stderr, 'waiting for a connection'

for i in xrange(0,n) :
    sock.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    server_address.append(('localhost', port))
    print >>sys.stderr, 'starting up on %s port %s' % server_address[i]
    sock[i].bind(server_address[i])
    sock[i].listen(1)
    connection[i], client_address[i] = sock[i].accept()
    print >>sys.stderr, 'connection from', client_address[i]
    idi[i] = connection[i].recv(256)
    print >>sys.stderr, '%s connected' % idi[i]
    port = port + 1

for i in xrange(0,n):
    connection[i].sendall(str(n))
    for j in xrange(0,n):
        if i != j :
            connection[i].sendall(idi[j])

def client(i):
    while True :
        name[i] = connection[i].recv(256)
        data[i] = connection[i].recv(256)
        print >>sys.stderr, 'received "%s"' % data[i]
        print >>sys.stderr, 'sending data back to the client'
        count[i] = len(re.findall(r'\w+', data[i]))

        if count[i] == 1 :
            iden[i] = 'server'
            data[i] = 'server'
        else :
            iden[i] = data[i].split(' ',1)[0]
            sent[i] = data[i].split(' ',1)[1]


        if iden[i] == "all" :
            for j in xrange(0,n) :
                if j != i :
                    connection[j].sendall(name[i])
                    connection[j].sendall('group')
                    connection[j].sendall(sent[i])

        elif iden[i] == 'server' and sent[i] == 'server' :
            connection[i].sendall('server')
            connection[i].sendall('alert')
            connection[i].sendall('User not found or Syntax error')

        elif iden[i] == 'list' and sent[i] == 'user' and count[i] == 2:
            connection[i].sendall('User Online :')
            for j in xrange(0,n):
                if i != j :
                    connection[i].sendall(idi[j])

        else :
            match = 0
            for j in xrange(0,n) :
                if iden[i] == idi[j] and i != j :
                    connection[j].sendall(name[i])
                    connection[j].sendall('private')
                    connection[j].sendall(sent[i])
                    match = 1
                    break
            if match == 0 :
                connection[i].sendall('server')
                connection[i].sendall('alert')
                connection[i].sendall('User not found or Syntax error')    

for x in xrange(0,n) :
    t[x] = threading.Thread(target=client, args=(x,))
    threads.append(t[x])
    t[x].start()

for q in threads :
    for tt in xrange(0,n) :
        t[tt].join()