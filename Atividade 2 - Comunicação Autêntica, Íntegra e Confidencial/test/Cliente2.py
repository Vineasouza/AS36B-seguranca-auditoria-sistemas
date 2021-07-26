# -*- coding: utf-8 -*-
#! /usr/bin/env python

import socket
import pickle
import sys
import time
import threading
import select
import traceback
from cryptography.fernet import Fernet
from hashlib import sha512
import hashlib
import rsa
import os.path

# Gera as chaves publica e privadas, retornando uma tupla (pub, priv)
# pub(n,e) | priv(n,e,d,p,q)
# n = valor de n = p*q, resultado da multiplicação de dois números primos grandes
# e = valor do expoente comum da chave => valor padrão: 65537
# d = valor da chave privada 
(pubkey2,privkey2) = rsa.newkeys(1024)
npublico_cliente2 = pubkey2.n
epublico_cliente2 = pubkey2.e
dprivado_client2 = privkey2.d
nprivado_client2 = privkey2.n

pubkey1 = None

class Server(threading.Thread):
    
    def initialise(self, receive):
        self.receive = receive

    def run(self):
        lis = []
        lis.append(self.receive)
        read, write, err = select.select(lis, [], [])
        global pubkey1

        # Loop de recebimento da chave publica do cliente 1
        # Armazena o n da chave publica do cliente 1 na variável npublico_client1
        for item in read: 
            try:
                s = item.recv(1024)
                if s != '':
                    npublico_client1 = int(s)
                else:
                    break
            except:
                traceback.print_exc(file=sys.stdout)
                break
        
        # Loop de recebimento da chave publica do cliente 1
        # Armazena o e da chave publica do cliente 1 na variável epublico_client1
        # Gera a chave publica do cliente 1 a partir do 'n' e do 'e' recebidos
        for item in read: 
            try:
                s = item.recv(1024)
                if s != '':
                    epublico_client1 = int(s)
                    pubkey1 = rsa.key.PublicKey(npublico_client1,epublico_client1)
                else:
                    break
            except:
                traceback.print_exc(file=sys.stdout)
                break
        
        # recebe a chave simétrica do cliente 1  cirptografada 
        # descriptografa a chave a partir da chave publica do cliente 2
        for item in read:
            try:
                s = item.recv(1024)
                if s != '':
                    keysimetricacriptografada = s
                    keysimetrica = rsa.decrypt(keysimetricacriptografada,privkey2)
                else:
                    break
            except:
                traceback.print_exc(file=sys.stdout)
                break
        
        #recebe e confere a assinatura da chave simétrica
        # recebe a assinatura do cliente 1 
        # verifica se a assinatura corresponde a chave simétrica recebida, a partir da chave assimetrica publica do cliente 1   
        # confirma o recebimento da chave simetrica do cliente 1
        for item in read:
            try:
                s = item.recv(1024)
                if s != '':
                    assi = s
                    if (rsa.verify(keysimetrica, assi, pubkey1)):
                        print('>> A chave simétrica foi recebida com sucesso << ')
                        sk = open('keysimetrica2.key','wb') #salva em um arquivo
                        sk.write(keysimetrica)                                                                                                      
                        sk.close()
                        f = Fernet(keysimetrica)
                        #envia um ok para finalizar o handshake
                        ok = "ok" 
                        self.receive.send(bytes(ok, encoding='utf8'))
                    else:
                        print('>> A chave simétrica não foi recebida com sucesso! <<')
                        exit()
            except:
                traceback.print_exc(file=sys.stdout)
                break
        
        # Loop de recebimento das mensagens  e da assinatura do cliente 1
        while 1:
            # 1 - recebe a mensagem criptografada
            # 2- utiliza a chave simétrica do cliente 1 recebida para descriptografar a mensagem
            for item in read:
                try:
                    s = item.recv(1024)
                    if s != '':
                        msgcriptografada = s
                        msg = f.decrypt(msgcriptografada).decode()    
                    else:
                        break
                except:
                    traceback.print_exc(file=sys.stdout)
                    break
            
            # 1- recebe a assinatura da mensagem
            # 2 - realiza a função digest (representação numérica de tamanho fixo do conteúdo de uma mensagem, 
            # calculada por uma função hash) da assinatura recebida e armazena na variavel 'hash_assinatura_client1'
            # 3 - realiza a verificação se a assinatura é valida 
            #   3.1 - realiza o calculo (assinatura^e) % n (sendo 'e' e 'n' recebidos anteriormente) e armazena na variavel 'assinatura_client2'
            #   3.2 - compara hashnovo com assi2novo para validar a assinatura
            #       3.2.1 - Se valida, imprime a mensagem
            #       3.2.2 - Se inválida, imprime um aviso  
            for item in read:
                try:
                    s = item.recv(1024)
                    if s != '':
                        assinatura_client1 = s
                        msgh = msg.encode()
                        hash_assinatura_client1 = int.from_bytes(hashlib.sha1(msgh).digest(), byteorder='big')
                        assinatura_nova_client1 = pow(int(assinatura_client1),epublico_client1,npublico_client1)
                        if(hash_assinatura_client1 == assinatura_nova_client1):
                            print(msg + '\n>> ')
                        else:
                            print('>> A mensagem não foi recebida de forma íntegra! <<')
                            exit()
                except:
                    traceback.print_exc(file=sys.stdout)
                    break

class Client(threading.Thread):

    def connect(self, host, port):
        self.sock.connect((host, port))

    def client(self, host, port, msg):
        sent = self.sock.send(msg)

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        try:
            host = input("Enter the server IP\n>> ")
            port = int(input("EEnter the server Destination Port\n>> "))
        except EOFError:
            print("Error")
            return 1
        print(">> Connecting <<\n")
        s = ''
        self.connect(host, port)
        print(">> Connected << \n")
        user_name = input("Enter the User Name to be Used:\n")
        time.sleep(1)
        srv = Server()
        srv.initialise(self.sock)
        srv.daemon = True
        print(">> Starting service << ")
        srv.start()

        # Ao iniciar o cliente, realiza o envio do valor de 'n' da chave publica do cliente 2 para o cliente 1
        self.client(host,port,bytes(str(npublico_cliente2), encoding='utf8'))
        time.sleep(1)

         # Realiza o envio do valor de 'e' da chave publica do cliente 2  e fica aguardando o recebimento da chave publica do cliente 1
        self.client(host,port,bytes(str(epublico_cliente2), encoding='utf8'))
        time.sleep(5)

        # Loop de verificação do handshake
        # Verifica se o arquivo 'keychavesimetrica2.key' ja existe e se exite algo gravado nele
        # Se sim, passa para o próximo passo, se não, continua aguardando o fim do handshake, com um intervalo de 10s
        while 1: #checa se já recebeu a chave simétrica
            if (os.path.isfile('keysimetrica2.key')): 
                if (os.path.getsize('keysimetrica2.key') > 0):
                    break
                else:
                    print("Aguardando Fim do Handshake...")
                    time.sleep(10)
            else:
                print("Aguardando Fim do Handshake...")
                time.sleep(10)
        
        # Loop de envio da mensagem, sendo ela delimitada a 255 caracteres
        # Para o envio da mensagem:
        # 1 - concatenado o valor de input de msg com o user_name definido e realizado o encode da msg
        
        # 4 - gerado a hash da mensagem utilizando o algoritmo SHA-1
        
        while 1:
            msg = input('>> ')
            if(len(msg)>256): #verificando se a mensagem possui mais de 255 caracteres
                print("Não é permitido enviar mensagem com mais de 255 caracteres!")
                break
            if msg == 'exit':
                break
            if msg == '':
                continue
            # 1 - concatenado o valor de input de msg com o user_name definido e realizado o encode da msg
            msg = user_name + ":" + msg
            msgh = msg.encode()

            #pega a chave simétrica de um arquivo
            # 2 - Abre e le o arquivo onde a chave simétrica foi armazenada e atribui ao Fernet
            simk = open('keysimetrica2.key','rb')
            keysimetrica = simk.read()
            f = Fernet(keysimetrica)

            # 3 - realiza a criptografia a partir da chave simétrica da mensagem utlizando fernet e **envia para o client 1**
            msgcriptografada = f.encrypt(msg.encode())
            self.client(host, port, msgcriptografada)
            time.sleep(2)
            # 4 - gerado a hash da mensagem utilizando o algoritmo SHA-1
            hash1 = int.from_bytes(hashlib.sha1(msgh).digest(), byteorder='big') 
            
            # 5 - gerando a assinatura a partir desta hash e dos valores de 'd' e 'n' do cliente 2 e **envia para o client 1**
             # realiza o calculo (hash^d) % n
            assinatura1 = pow(hash1,dprivado_client2,nprivado_client2)
            self.client(host,port,bytes(str(assinatura1), encoding='utf8'))
            time.sleep(5)
        return (1)

if __name__ == '__main__':
    print(">> Starting client <<")
    cli = Client()
    cli.start()