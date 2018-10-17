def encrypt_caesar(plaintext):
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ''
    for lit in plaintext:
        if 'A' <= lit <= 'Z' or 'a' <= lit <= 'z':
            if lit >= 'X' and lit <= 'Z' or lit >= 'x' and lit <= 'z':
                ciphertext += chr(ord(lit)+3-26)
            else:
                ciphertext += chr(ord(lit)+3)
        else:
            ciphertext += lit
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ''
    for lit in ciphertext:
        if 'A' <= lit <= 'Z' or 'a' <= lit <= 'z':
            if lit >= 'A' and lit <= 'C' or lit >= 'a' and lit <= 'c':
                plaintext += chr(ord(lit) - 3 + 26)
            else:
                plaintext += chr(ord(lit) - 3)
        else:
            plaintext += lit
    return plaintext
