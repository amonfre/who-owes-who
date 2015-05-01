''' A simple implementation of RSA cryptosystem

Usage:
    
1. Key generation.
Create a random public-private key pair with command:
    
	public_key, private_key = keygen_pair(5)

where the argument is length of key. The higher the length, the stronger the
encryption, should be at least equal to or higher than 5. 

2. Encryption.
The generated public key can be used to encrypt messages,
which in our case is a transaction - a positive integer number:

	trans = 5
	encrypted_trans = public_key.encrypt(trans)

3. Decryption. 
The encrypted information can only be retrieved with the generated private key:

	private_key.decrypt(encrypted_trans)

would return the transaction, which is 5. 

'''

import random
from collections import namedtuple

''' Part 1: Key generation '''

def relatively_prime(x, y):
    ''' Helper function that returns True if a and b are two relatively
    prime numbers : if they have no factors in common other than 1. '''
    
    for n in range(2, min(x, y) + 1):
        if x % n == y % n == 0:
            return False
    return True


def return_primes(begin, end):
    ''' Helper function that returns a list of 
        prime numbers within the given range (begin, end). '''

    if begin >= end:
        return []

    primes = [2]

    for x in range(3, end + 1, 2):
        for p in primes:
            if x % p == 0:
                break
        else:
            primes.append(x)

    while primes and primes[0] < begin:
        del primes[0]

    return primes


def keygen_pair(length):
    ''' The main function that creates a public-private key pair.
    The key pair is generated from two random prime numbers. Length
    specifies the bit length of the number n shared between the two keys.
    '''

    length = random.randint(5,20)

    if length < 5:
        raise ValueError('cannot generate a key of length less '
                         'than 5 (got {!r})'.format(length))

    # First, we choose two prime numbers p and q to compute n,
    # which is the modulus for both the public and private keys.
    # n must obey the length argument specified so
    # it must be in range(n_min, n_max + 1)
    # The numbers p and q should be chosen at random,
    # and be of similar bit-length for security purposes.
    # We will choose two prime numbers in range(begin, end) so that the
    # difference of bit lengths is at most 2.

    n_min = 1 << (length - 1)
    n_max = (1 << length) - 1

    begin = 1 << (length // 2 - 1)
    end = 1 << (length // 2 + 1)
    primes = return_primes(begin, end)

    # Random selection of two numbers so that their 
    # product is in range(n_min, n_max + 1).
    while primes:
        p = random.choice(primes)
        primes.remove(p)
        q_options = [q for q in primes
                        if n_min <= p * q <= n_max]
        if q_options:
            q = random.choice(q_options)
            break
    else:
        raise AssertionError("cannot find 'p' and 'q' for a key of "
                             "length={!r}".format(length))

    # Secondly, we choose an integer e that satisfies 1 < e < (p - 1) * (q - 1)
    # and is coprime with (p - 1) * (q - 1).
    end = (p - 1) * (q - 1)
    for e in range(3, end, 2):
        if relatively_prime(e, end):
            break
    else:
        raise AssertionError("cannot find 'e' with p={!r} "
                             "and q={!r}".format(p, q))


    # Third, we find d such that it is the modular multiplicative inverse of e
    for d in range(3, end, 2):
        if d * e % end == 1:
            break
    else:
        raise AssertionError("cannot find 'd' with p={!r}, q={!r} "
                             "and e={!r}".format(p, q, e))

    # Finally, we can build and return the public and private keys.
    # The public key consists of n and e, the private key consists of n and d.
    n = p * q
    return PublicKey(n, e), PrivateKey(n, d)


""" Part 2: Encryption """

class PublicKey(namedtuple('PublicKey', 'n e')):
    ''' Public key which can be used to encrypt data. '''

    def encrypt(self, x):
        ''' Encrypts the number x and returns a number which can only be
        decrypted using the private key.
        '''
        return pow(x, self.e, self.n)

""" Part 3: Decryption """

class PrivateKey(namedtuple('PrivateKey', 'n d')):
    """ Private key which can be used both to decrypt data."""

    def decrypt(self, x):
        ''' Decrypts the number x and returns the 
        original message which was encrypted with public key. 
        '''
        return pow(x, self.d, self.n)