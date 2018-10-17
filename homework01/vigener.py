def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    # PUT YOUR CODE HERE
    i = 0
    ciphertext = ''
    for lit in plaintext:
        if 'A' <= lit <= 'Z' or 'a' <= lit <= 'z':
            if i > len(keyword)-1:
                i = 0
            if 'A' <= keyword[i] <= 'Z':
                lit1 = ord(lit) + (ord(keyword[i])-65)
                if lit1 > ord('Z'):
                    lit1 -= 26
            elif 'a' <= keyword[i] <= 'z':
                lit1 = ord(lit) + (ord(keyword[i])-97)
                if ord('Z') < lit1 < ord('a') or lit1 > ord('z'):
                    lit1 -= 26
        i += 1
        ciphertext += chr(lit1)
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    # PUT YOUR CODE HERE
    i = 0
    plaintext = ''
    for lit in ciphertext:
        if 'A' <= lit <= 'Z' or 'a' <= lit <= 'z':
            if i > len(keyword) - 1:
                i = 0
            if 'A' <= keyword[i] <= 'Z':
                lit1 = ord(lit) - (ord(keyword[i]) - 65)
                if lit1 < ord('A'):
                    lit1 += 26
            elif 'a' <= keyword[i] <= 'z':
                lit1 = ord(lit) - (ord(keyword[i]) - 97)
                if lit1 < ord('A') or ord('Z') < lit1 < ord('a'):
                    lit1 += 26
        i += 1
        plaintext += chr(lit1)
    return plaintext
