from cryptography.fernet import Fernet


KEY_GEN = "test"

def encrypt(msg):
    fernet = Fernet(KEY_GEN)
    return fernet.encrypt(msg.encode())
  
def decrypt(msg):
    fernet = Fernet(KEY_GEN)
    return fernet.decrypt(msg, ttl=60).decode()

def print_KEY():
    print(KEY_GEN)


if __name__ == '__main__':
    KEY_GEN = Fernet.generate_key()
    
    msg = "Ola mundo"
    print(msg)

    encMsg = encrypt(msg)
    print(encMsg)

    decMsg = decrypt(encMsg)
    print(decMsg)

    

