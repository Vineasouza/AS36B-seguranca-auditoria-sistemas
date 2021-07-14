import pickle
import rsa

# Generates public and private keys, and returns them as (pub, priv).
def genRSAKey(nbits : int):
    try:
        return rsa.newkeys(nbits=nbits, poolsize=8)
    except: 
        raise ValueError

if __name__ == '__main__':
    msg1 = 'hi'
    msg2 = 'hello'
    dumb = [msg1,msg2]

    data = pickle.dumps(dumb)

    show = pickle.loads(data)
    print(show)

