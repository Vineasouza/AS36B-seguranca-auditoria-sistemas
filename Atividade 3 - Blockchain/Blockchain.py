# https://www.activestate.com/blog/how-to-build-a-blockchain-in-python/
import os
import sys
import time
import json
import requests
from hashlib import sha256
from datetime import timedelta
from flask import Flask, request
from timeit import default_timer as timer

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    # difficulty of our PoW algorithm
    difficulty : 1

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True
    
    def setDifficulty(self, dffclty):
        Blockchain.difficulty = dffclty

    def is_valid_proof(self, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def proof_of_work(self, block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        t_proof = time.process_time()
        proof = self.proof_of_work(new_block)
        elapsed_time_proof = time.process_time() - t_proof
        print("\n\tTempo de PoW do bloco: " + str(elapsed_time_proof) + "s")

        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        return new_block.index


def add_chain_transaction(transaction):
    """
    Fun????o que recebe uma transa????o, adiciona a lista de transa????es 
    e adiciona um novo bloco a partir desta transa????o, realizando o
    Proof of Work e verificando se o PoW ?? v??lido

    """
    blockchain.add_new_transaction(transaction)
    blockchain.mine()

def show_all_chains():
    """
    Fun????o que mostra todos os blocos da blockchain
    """
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    chains = json.dumps({"length": len(chain_data),"chain": chain_data}, indent=2, sort_keys=True) 
    print(chains)

def show_specific_chain(index: int):
    """
    Fun????o que mostra um bloco espec??fico da blockchain
    """
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    chain_specific= json.dumps(chain_data[index], indent=2, sort_keys=True) 
    print(chain_specific)

def show_last_chain():
    """
    Fun????o que mostra o ultimo bloco da blockchain
    """
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    chain_last= json.dumps(chain_data[blockchain.last_block.index], indent=2, sort_keys=True) 
    print(chain_last)

def PoW(index : int):
    """
    Teste de prova de trabalho de um bloco espec??fico
    """
    # Percorre todas os blocos para encontrar o bloco com o index requerido
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    x = chain_data[index]
    block = Block(index=index, transactions=x["transactions"], timestamp=x["timestamp"], previous_hash=x["previous_hash"])

    # mostra o
    print("\tPrev hash: " + x["previous_hash"])

    # Fun????o que tenta diferentes valores de nonce para obter um hash que satisfa??a nossos crit??rios de dificuldade
    # printando o tempo requerido
    t_proof = time.process_time()
    proof_hash = blockchain.proof_of_work(block)
    elapsed_time_proof = time.process_time() - t_proof
    print("\n\tProof hash: " + proof_hash)
    print("\tTempo de PoW do bloco: " + str(elapsed_time_proof) + "s\n")

    # Verifica se block_hash ?? um hash de bloco v??lido e satisfaz os crit??rios de dificuldade
    # printando o tempo requerido
    v_proof = time.process_time()
    valid_proof = blockchain.is_valid_proof(block, proof_hash)
    elapsed_time_proof_v = time.process_time() - v_proof
    print("\n\tIs valid proof: " + str(valid_proof))
    print("\tTempo de valida????o do PoW do bloco: " + str(elapsed_time_proof_v) + "s\n")

def validateAllBlocks():
    """
    Rotina para validar todos os blocos 
    """
    # Armazena todos os blocos existentes no array chain_data
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)

    # Percorre o array realizando o PoW e a valida????o de cada bloco
    for i in range(blockchain.last_block.index):
        print("\n\n\tValidando bloco: " + str(i) + " de " + str(blockchain.last_block.index - 1) + " blocos")
        x = chain_data[i]
        print("\tPrev hash: " + x["previous_hash"])
        block = Block(index=i, transactions=x["transactions"], timestamp=x["timestamp"], previous_hash=x["previous_hash"])
        proof_hash = blockchain.proof_of_work(block)
        print("\tProof hash: " + proof_hash)
        valid_proof = blockchain.is_valid_proof(block, proof_hash)
        print("\tIs valid proof - bloco " + str(i) + ": " + str(valid_proof))

def changeValueOf(idx : int, newValue : int):
    """
    Fun????o que permite mudar o valor de um bloco e revalida todos os blocos que dependem dele 
    """
    chain_data = []
    chain_aux_1 = []
    chain_aux_2 = []

    # Verifica se o index ?? zero
    if (int(idx) == 0): raise IndexError

    # Armazena todos os blocos existentes no array chain_data
    for block in blockchain.chain:
        chain_data.append(block.__dict__)

    # Retira todos os blocos que est??o entre o final e o index recebido, passando o valor para o array auxiliar
    for i in range(int(idx), len(blockchain.chain)):
        chain_aux_1.append(blockchain.chain.pop((int(idx))))

    # varre o array auxiliar 1, verificando que sempre o valor do index do valor a ser mudado ?? o 0 e seta o novo valor
    # caso nao for o index do valor a ser modificado, apenas passa o atributo da lista para o array auxiliar 2
    for i in range(len(chain_aux_1)):
        if(i == 0):
            setattr(chain_aux_1[i], "transactions", newValue)
        chain_aux_2.append(getattr(chain_aux_1[i],"transactions"))
    
    clearCMD()
    print("\n\t************************************************")
    print("\n\tRevalidando Blocos")
    print("\n\t************************************************")
    

    # Percorre o array auxiliar 2, verificando se a posi????o possui um int ou um list
    # Envia o valor para a fun????o que adicionar um novo bloco a Blockchain
    for i in range(len(chain_aux_2)):
        x = 0
        if(type(chain_aux_2[i]) == int):
            x = chain_aux_2[i]
            add_chain_transaction(x)
        elif(type(chain_aux_2[i]) == list):
            x = chain_aux_2[i]
            add_chain_transaction(x[0])
    
    print("\n\n\t************************************************")
    print("\n\tBlocos Revalidados, Blockchain como novo valor pronta!")
    print("\n\t************************************************")
    input("\n\t>>Pressione enter<<")

    show_all_chains()

def clearCMD():
    """
    Limpa o terminal
    """
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    blockchain = Blockchain()

    clearCMD()
    dffclty = input("\n\tDefina a dificuldade >> ")
    blockchain.setDifficulty(int(dffclty))

    while(1):
        clearCMD()
        # ********************************************************* MENU ********************************************************** #
        print("\t************************************************")
        print("\t1 - Adicionar uma transa????o")
        print("\t2 - Mostrar todos os blocos")
        print("\t3 - Mostrar um bloco de index especif??co")
        print("\t4 - Mostrar o ultimo bloco ")
        print("\t5 - PoW bloco espec??fico ")
        print("\t6 - Mudar o valor de um bloco espec??fico ")
        print("\t7 - Rotina de valida????o de todos os blocos")
        print("\t8 - Mudar dificuldade ")
        print("\texit - Sair da aplica????o")
        print("\t************************************************")
        opt = input("\n\tEscolha uma op????o >> ")
        
        # ********************************************************* OPT 1 ********************************************************* #
        if(opt == '1'):
            clearCMD()
            trx = input("\tInsira uma transa????o num??rica >> ")
            if(trx.isdigit() and len(trx) > 0):
                add_chain_transaction(trx)
            else:
                clearCMD()
                print("\n\t************************************************")
                print("\n\tValor Inv??lido")  
            print("\n\t************************************************")
            sair = input("\n\tEnter para voltar para o menu ")
        
        # ********************************************************* OPT 2 ********************************************************* #
        elif(opt == '2'):
            clearCMD()
            show_all_chains()
            print("\n\t************************************************")
            sair = input("\n\tEnter para voltar para o menu ")
        
        # ********************************************************* OPT 3 ********************************************************* #
        elif(opt == '3'):
            clearCMD()
            idx = input("\tEscolha um index de 0 ate " + str(blockchain.last_block.index) + " >> ")
            if(idx.isdigit() and int(idx) <= blockchain.last_block.index):
                show_specific_chain(int(idx))
            else:
                clearCMD()
                print("\n\t************************************************")
                print("\n\tValor Inv??lido")
            print("\n\t************************************************")
            sair = input("\n\tEnter para voltar para o menu ")
        
        # ********************************************************* OPT 4 ********************************************************* #
        elif(opt == '4'):
            clearCMD()
            show_last_chain()
            print("\n\t************************************************")
            sair = input("\n\tEnter para voltar para o menu ")
        
        # ********************************************************* OPT 5 ********************************************************* #
        elif(opt == '5'):
            clearCMD() 
            idx = input("\tEscolha um index de 0 ate " + str(blockchain.last_block.index) + " >> ")
            if(idx.isdigit() and int(idx) <= blockchain.last_block.index):
                PoW(int(idx))
            else:
                clearCMD()
                print("\n\t************************************************")
                print("\n\tValor Inv??lido")
            print("\n\t************************************************")
            sair = input("\n\tEnter para voltar para o menu ")
        
        # ********************************************************* OPT 6 ********************************************************* #
        elif(opt == '6'):
            clearCMD()
            idx = input("\tEscolha um index de 1 ate " + str(blockchain.last_block.index) + " do bloco que deseja mudar o valor >> ")
            newValue = input("\tDigite o novo valor do bloco >> ")
            if(int(idx) > 0 and newValue.isdigit() and idx.isdigit() and int(idx) <= blockchain.last_block.index):
                changeValueOf(int(idx), int(newValue))
            else:
                clearCMD()
                print("\n\t************************************************")
                print("\n\tValor Inv??lido")
            print("\n\t************************************************")
            sair = input("\n\tEnter para voltar para o menu ")
        
        # ********************************************************* OPT 7 ********************************************************* #
        elif(opt == '7'):
            clearCMD()
            validateAllBlocks()
            print("\n\t************************************************")
            sair = input("\n\tEnter para voltar para o menu ")

        # ********************************************************* OPT 8 ********************************************************* #
        elif(opt == '8'):
            clearCMD()
            dffclty = input("\tDefina a dificuldade >> ")
            blockchain.setDifficulty(int(dffclty)) 
            print("\n\t************************************************")
            sair = input("\n\tEnter para voltar para o menu ")

        # ******************************************************* OPT EXIT ******************************************************** #
        elif(opt == 'exit'):
            clearCMD()
            sys.exit()
        
        # ******************************************************* DEFAULT ********************************************************* #
        else:
            clearCMD()
            print("\n\t************************************************")
            print("\n\tEscolha uma op????o v??lida")
            print("\n\t************************************************")
            sair = input("\n\tEnter para voltar para o menu ")


# -----------------------------------------------------#
# app = Flask(__name__)
# blockchain = Blockchain()

# @app.route('/chain', methods=['GET'])
# def get_chain():
#     chain_data = []
#     for block in blockchain.chain:
#         chain_data.append(block.__dict__)
#     return json.dumps({"length": len(chain_data),
#                        "chain": chain_data})

# app.run(debug=True, port=5000)
# -----------------------------------------------------#
