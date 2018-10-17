import random


def is_prime(n):
    """
    Tests to see if a number is prime.
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    f = int(n**0.5+1)
    for i in range(2, f):
        if (n % i == 0):
            return False
    return True


def gcd(a, b):
    """
    Euclid's algorithm for determining the greatest common divisor.
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a + b


def multiplicative_inverse(e, phi):
    """
    Euclid's extended algorithm for finding the multiplicative
    inverse of two numbers.
    >>> multiplicative_inverse(7, 40)
    23
    """
    phi, e = e, phi
    tabl = []
    tabl.append([e, phi, e % phi, e // phi])
    while (e % phi != 0):
        c = e % phi
        e = phi
        phi = c
        tabl.append([e, phi, e % phi, e // phi])
    tabl[-1].extend([0, 1])
    i = -1
    while tabl[0][0] != tabl[i][0]:
        i -= 1
        x = tabl[i + 1][5]
        y = tabl[i + 1][4] - tabl[i + 1][5] * tabl[i][3]
        tabl[i].extend([x, y])
    d = tabl[0][-1] % tabl[0][0]
    return d


def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    n = p*q
    phi = (p-1)*(q-1)
    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)
    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def encrypt(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on
    # the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)


if __name__ == '__main__':
    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
