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
    Função que recebe uma transação, adiciona a lista de transações 
    e adiciona um novo bloco a partir desta transação, realizando o
    Proof of Work e verificando se o PoW é válido

    """
    blockchain.add_new_transaction(transaction)
    blockchain.mine()

def show_all_chains():
    """
    Função que mostra todos os blocos da blockchain
    """
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    chains = json.dumps({"length": len(chain_data),"chain": chain_data}, indent=2, sort_keys=True) 
    print(chains)

def show_specific_chain(index: int):
    """
    Função que mostra um bloco específico da blockchain
    """
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    chain_specific= json.dumps(chain_data[index], indent=2, sort_keys=True) 
    print(chain_specific)

def show_last_chain():
    """
    Função que mostra o ultimo bloco da blockchain
    """
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    chain_last= json.dumps(chain_data[blockchain.last_block.index], indent=2, sort_keys=True) 
    print(chain_last)

def clearCMD():
    """
    Limpa o terminal
    """
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    blockchain = Blockchain()

    dffclty = input("\n\tDefina a dificuldade >> ")
    blockchain.setDifficulty(int(dffclty))

    while(1):
        clearCMD()
        print("\t************************************************")
        print("\t1 - Adicionar uma transação")
        print("\t2 - Mostrar todos os blocos")
        print("\t3 - Mostrar um bloco de index especifíco")
        print("\t4 - Mostrar o ultimo bloco ")
        print("\texit - Sair da aplicação")
        print("\t************************************************")
        opt = input("\n\tEscolha uma opção >> ")
        
        if(opt == '1'):
            clearCMD()
            trx = input("\tInsira uma transação >> ")
            add_chain_transaction(trx)
            print("\n\t************************************************")
            sair = input("\n\tEnter para voltar para o menu ")
        
        elif(opt == '2'):
            clearCMD()
            show_all_chains()
            print("\n\t************************************************")
            sair = input("\n\tEnter para voltar para o menu ")
        
        elif(opt == '3'):
            clearCMD()
            idx = input("\tEscolha um index de 0 ate " + str(blockchain.last_block.index) + " >> ")
            if(int(idx) <= blockchain.last_block.index):
                show_specific_chain(int(idx))
            else:
                clearCMD()
                print("\n\t************************************************")
                print("\n\tValor Inválido")
            print("\n\t************************************************")
            sair = input("\n\tEnter para voltar para o menu ")
        
        elif(opt == '4'):
            clearCMD()
            show_last_chain()
            print("\n\t************************************************")
            sair = input("\n\tEnter para voltar para o menu ")
        
        elif(opt == 'exit'):
            clearCMD()
            sys.exit()
        
        else:
            clearCMD()
            print("\n\t************************************************")
            print("\n\tEscolha uma opção válida")
            print("\n\t************************************************")
            sair = input("\n\tEnter para voltar para o menu ")




# blockchain.is_valid_proof(blockchain.last_block,blockchain.proof_of_work(blockchain.last_block) )  

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

