#! /usr/bin/env python

import socket
import sys
import time
import threading
import select
import traceback
from cryptography.fernet import Fernet

# Função responsável por abrir o arquivo e ler o arquivo, e retornar a chave secreta
def read_key():
    f = open("key.txt", "r")
    return f.read().encode()

#Função responsável por receber uma string e uma chave secreta, retornando o conteúdo criptografado
def encrypt(msg, key):
    fernet = Fernet(key)
    return fernet.encrypt(msg.encode())

#Função responsável por receber uma mensagem criptografada e uma chave secreta, retornando o conteúdo descriptografado
def decrypt(msg, key):
    fernet = Fernet(key)
    return fernet.decrypt(msg, ttl=10000).decode()


class Server(threading.Thread):
    def initialise(self, receive):
        self.receive = receive

    def run(self):
        lis = []
        lis.append(self.receive)
        while 1:
            #recebe a mensagem
            read, write, err = select.select(lis, [], [])
            for item in read:
                try:
                    s = item.recv(4096)
                    if s != '':
                        chunk = s #própria mensagem recebida se nao vazia                        
                        print(decrypt(chunk, read_key()) + '\n>>')  #descriptografa a mensagem recebida chamado a função e exibe o conteúdo
                except:
                    traceback.print_exc(file=sys.stdout)
                    break


class Client(threading.Thread):
    def connect(self, host, port):
        self.sock.connect((host, port))

    def client(self, host, port, msg):
        sent = self.sock.send(msg)
        # print "Sent\n"

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        try:
            host = input("Enter the server IP \n>>")
            port = int(input("Enter the server Destination Port\n>>"))
        except EOFError:
            print("Error")
            return 1

        print("Connecting\n")
        s = ''
        self.connect(host, port)
        print("Connected\n")
        user_name = input("Enter the User Name to be Used\n>>")
        receive = self.sock
        time.sleep(1)
        srv = Server()
        srv.initialise(receive)
        srv.daemon = True
        print("Starting service")
        srv.start()
        while 1:
            # print "Waiting for message\n"
            msg = input('>>') #mensagem a ser enviada
            if msg == 'exit':
                break
            if msg == '':
                continue
            # print "Sending\n"
            msg = user_name + ': ' + msg 
            data = encrypt(msg, read_key())  #criptografa a mensagem utilizando a função e armazana o conteúdo na variavel data
            self.client(host, port, data)
        return (1)


if __name__ == '__main__':
    print("Starting client")
    cli = Client()
    cli.start()