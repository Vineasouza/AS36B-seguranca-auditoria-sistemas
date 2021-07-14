#https://stuvel.eu/python-rsa-doc/usage.html
import rsa

# Generates public and private keys, and returns them as (pub, priv).
def genRSAKey(nbits : int):
    try:
        return rsa.newkeys(nbits=nbits, poolsize=8)
    except: 
        raise ValueError

# Encrypt message with public key | Encrypts the given message using PKCS#1 v1.5
def cryptMsg(msg : bytes, pbKey):
    try:
        return rsa.encrypt(msg, pbKey)
    except:
        raise ValueError

# Decrypt message with private key | Decrypts the given message using PKCS#1 v1.5
def decryptMsg(msg : bytes, pvKey):
    try:
        return rsa.decrypt(msg, pvKey)
    except:
        raise rsa.DecryptionError('Decryption failed')

# Returns the message digest.
def genHash(msg : bytes, hshType: str):
    try:
        return rsa.compute_hash(msg, hshType)
    except:
        raise ValueError

# Signs a precomputed hash with the private key.
def genSignature(hash : bytes, pvKey, hshType: str):
    try:
        return rsa.sign_hash(hash, pvKey, hshType)
    except:
        raise ValueError

# Verifies that the signature matches the message.
def verifySignature(msg : bytes, sign: bytes, pbKey):
    try:
        return rsa.verify(msg, sign, pbKey)
    except:
        raise rsa.VerificationError('Verification failed')

if __name__ == '__main__':
    (pubkey, privkey) = genRSAKey(512)

    message = 'Teste de comunicação'.encode()

    # types: 'MD5', 'SHA-1', 'SHA-224', SHA-256', 'SHA-384' or 'SHA-512'
    hshType = 'SHA-256'

    msgCrypt = cryptMsg(message, pubkey)

    hash = genHash(msgCrypt, hshType)

    signature = genSignature(hash, privkey, hshType)

    if(verifySignature(msgCrypt, signature, pubkey)):
        print("Verification pass")
        msgDecrypt = decryptMsg(msgCrypt, privkey)
        print("Message Decrypt: " + msgDecrypt.decode())
    else:
         raise rsa.VerificationError('Verification failed')

