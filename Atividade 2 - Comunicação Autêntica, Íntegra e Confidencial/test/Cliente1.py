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
(pubkey1,privkey1) = rsa.newkeys(1024)
npublico_client1 = pubkey1.n
epublico_client1 = pubkey1.e
dprivado_client1 = privkey1.d
nprivado_client1 = privkey1.n
pubkey2 = None

SOCKET_LIST = []

class Server(threading.Thread):
    
    def initialise(self, receive):
        self.receive = receive

    def run(self):
        lis = []
        lis.append(self.receive)
        read, write, err = select.select(lis, [], [])
        global pubkey2
        
        # Loop de recebimento da chave publica do cliente 2
        # Armazena o n da chave publica do cliente 2 na variável npublico_client2
        for item in read: 
            try:
                s = item.recv(1024)
                if s != '':
                    npublico_client2 = int(s)
                else:
                    break
            except:
                traceback.print_exc(file=sys.stdout)
                break
        
        # Loop de recebimento da chave publica do cliente 2
        # Armazena o e da chave publica do cliente 2 na variável epublico_client2
        # Gera a chave publica do cliente 2 a partir do 'n' e do 'e' recebidos
        for item in read: 
            try:
                s = item.recv(1024)
                if s != '':
                    epublico_client2 = int(s)
                    pubkey2 = rsa.key.PublicKey(npublico_client2,epublico_client2)
                else:
                    break
            except:
                traceback.print_exc(file=sys.stdout)
                break
        
        # Após o recebimento dos valores de 'n' e 'e' da chave publica do cliente 2,
        # recebe um ok do cliente 2, sendo ele gravado no arquivo 'ok1.txt' 
        # para posterior finalização do handshake entre os clientes
        for item in read:
            try:
                s = item.recv(1024)
                if s != '':
                    # Le o valor 'Ok' e grava no arquivo 'ok1.txt'
                    ok = s
                    k = open('ok1.txt','wb')
                    k.write(ok)
                    k.close()
                else:
                    break
            except:
                traceback.print_exc(file=sys.stdout)
                break

        # Loop de recebimento das mensagens e da assinatura do cliente 2
        while 1:
            # 1 - recebe a mensagem criptografada
            # 2 - abre e le o arquivo onde a chave simetrica do cliente foi gravada e aramazena na variavel chave_simetrica_client1
            # 3 - utiliza a chave simétrica para descriptografar a mensagem
            for item in read:
                try:
                    s = item.recv(1024)
                    if s != '':
                        msgcriptografada = s
                        arq_chave_simetrica = open('keysimetrica.key','rb')
                        chave_simetrica_client1 = arq_chave_simetrica.read()
                        f = Fernet(chave_simetrica_client1)
                        msg = f.decrypt(msgcriptografada).decode()    
                    else:
                        break
                except:
                    traceback.print_exc(file=sys.stdout)
                    break
            
            # 1 - recebe a assinatura da mensagem
            # 2 - realiza a função digest (representação numérica de tamanho fixo do conteúdo de uma mensagem, 
            # calculada por uma função hash) da assinatura recebida e armazena na variavel 'hash_assinatura_client2'
            # 3 - realiza a verificação se a assinatura é valida 
            #   3.1 - realiza o calculo (assinatura^e) % n (sendo 'e' e 'n' recebidos anteriormente) e armazena na variavel 'assinatura_client2'
            #   3.2 - compara hashnovo com assi2novo para validar a assinatura
            #       3.2.1 - Se valida, imprime a mensagem
            #       3.2.2 - Se inválida, imprime um aviso  
            for item in read:
                try:
                    s = item.recv(1024)
                    if s != '':
                        assinatura_client2 = s
                        msgh = msg.encode()
                        hash_assinatura_client2 = int.from_bytes(hashlib.sha1(msgh).digest(), byteorder='big')
                        assinatura_nova_client2 = pow(int(assinatura_client2),epublico_client2,npublico_client2)
                        if(hash_assinatura_client2 == assinatura_nova_client2):
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
        user_name = input("Enter the User Name to be Used\n>> ")
        time.sleep(1)
        srv = Server()
        srv.initialise(self.sock)
        srv.daemon = True
        print(">> Starting service << ")
        srv.start()
        SOCKET_LIST.append(self.sock)


        # Ao iniciar o cliente, realiza o envio do valor de 'n' da chave publica do cliente1 para o cliente 2
        self.client(host,port,bytes(str(npublico_client1), encoding='utf8'))
        time.sleep(1)


        # Realiza o envio do valor de 'e' da chave publica do cliente 1  e fica aguardando o recebimento da chave publica do cliente 2
        self.client(host,port,bytes(str(epublico_client1), encoding='utf8'))
        time.sleep(3)
        
        # Gera uma chave simétrica, armazenando-a no arquivo 'keyssimetrica.key' e 
        # realiza o envio desta chave , criptografando-a  a partir da chave publica do cliente 2
        keysimetrica = Fernet.generate_key()
        f = Fernet(keysimetrica)
        sk = open('keysimetrica.key','wb') #salva em um arquivo
        sk.write(keysimetrica)                                                                                                      
        sk.close()
        simkeycripto = rsa.encrypt(keysimetrica,pubkey2)
        self.client(host,port,simkeycripto)
        time.sleep(4)

        # cria o hash e a assinatura da chave e o envia
        # Gera o hash utilizando o algoritmo SHA-1 a partir da chave simétrica
        # gerando assim a assinatura do cliente e realiza o envio para o cliente 2
        hash1 = rsa.compute_hash(keysimetrica, 'SHA-1') 
        assinatura = rsa.sign_hash(hash1, privkey1, 'SHA-1')
        self.client(host,port,assinatura)
        time.sleep(5)

        # Loop de verificação do handshake
        # Verifica se o arquivo 'ok1.txt' ja existe e se existe algo gravado nele
        # Se sim, passa para o próximo passo, se não, continua aguardando o fim do handshake, com um intervalo de 10s
        while 1: #checa se já acabou o handshake
            if (os.path.isfile('ok1.txt')): 
                if (os.path.getsize('ok1.txt') > 0):
                    break
                else:
                    print(">> Aguardando Fim do Handshake... <<")
                    time.sleep(10)
            else:
                print(">> Aguardando Fim do Handshake... <<")
                time.sleep(10)
        
        # Loop de envio da mensagem, sendo ela delimitada a 255 caracteres
        # Para o envio da mensagem:      
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

            # 2 - realizada a criptografia da mensagem utlizando fernet e **envia para o client 2**
            msgcriptografada = f.encrypt(msg.encode())
            self.client(host, port, msgcriptografada)
            time.sleep(2)

            # 3 - gerado a hash da mensagem utilizando o algoritmo SHA-1
            hash2= int.from_bytes(hashlib.sha1(msgh).digest(), byteorder='big') 
            
            # 4 - gerando a assinatura a partir desta hash e dos valores de 'd' e 'n' do cliente 1 e **envia para o client 2**
            # realiza o calculo (hash^d) % n
            assinatura2 = pow(hash2,dprivado_client1,nprivado_client1)
            self.client(host,port,bytes(str(assinatura2), encoding='utf8'))
            time.sleep(5)
        return (1)

if __name__ == '__main__':
    print(">> Starting client <<")
    cli = Client()
    cli.start()