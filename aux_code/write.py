from cryptography.fernet import Fernet

if __name__ == '__main__':
    KEY_GEN = Fernet.generate_key()
    print(KEY_GEN)
    f = open("key.txt", "w")
    f.write(KEY_GEN.decode())
    f.close()

    f = open("key.txt", "r")
    print(f.read().encode())