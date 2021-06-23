#! /usr/bin/env python

import socket
import sys
import traceback
import threading
import select
from cryptography.fernet import Fernet

SOCKET_LIST = []
TO_BE_SENT = []
SENT_BY = {}

# Função responsável por:
#  - gera uma chave secreta e armazenar na variável KEY_GEN  
# - abrir um arquivo e gravar o conteúdo da variável KEY_GEN  
def write_key():
    KEY_GEN = Fernet.generate_key()
    f = open("key.txt", "w")
    f.write(KEY_GEN.decode())
    f.close()


class Server(threading.Thread):

    def init(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.bind(('', 5535))
        self.sock.listen(2)
        SOCKET_LIST.append(self.sock)
        print("Server started on port 5535")

    def run(self):
        while 1:
            read, write, err = select.select(SOCKET_LIST, [], [], 0)
            for sock in read:
                if sock == self.sock:
                    sockfd, addr = self.sock.accept()
                    print(str(addr))

                    SOCKET_LIST.append(sockfd)
                    print(SOCKET_LIST[len(SOCKET_LIST) - 1])

                else:
                    try:
                        s = sock.recv(4096)
                        if s == '':
                            print(str(sock.getpeername()))
                            continue
                        else:
                            TO_BE_SENT.append(s)
                            SENT_BY[s] = (str(sock.getpeername()))
                    except:
                        print(str(sock.getpeername()))


class handle_connections(threading.Thread):
    def run(self):
        while 1:
            read, write, err = select.select([], SOCKET_LIST, [], 0)
            for items in TO_BE_SENT:
                for s in write:
                    try:
                        if (str(s.getpeername()) == SENT_BY[items]):
                            print("Ignoring %s" % (str(s.getpeername())))
                            continue
                        print("Sending to %s" % (str(s.getpeername())))
                        s.send(items) #envio da mensagem para o cliente, sendo ITEMS a mensagem

                    except:
                        traceback.print_exc(file=sys.stdout)
                TO_BE_SENT.remove(items)
                del (SENT_BY[items])


if __name__ == '__main__':
    write_key()
    srv = Server()
    srv.init()
    srv.start()
    print(SOCKET_LIST)
    handle = handle_connections()
    handle.start()