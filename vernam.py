import string
import re
from collections import Counter

BAUDOT_CODE = {
    0: '\0',
    1: 'T',
    2: '\r',
    3: 'O',
    4: ' ',
    5: 'H',
    6: 'N',
    7: 'M',
    8: '\n',
    9: 'L',
    10: 'R',
    11: 'G',
    12: 'I',
    13: 'P',
    14: 'C',
    15: 'V',
    16: 'E',
    17: 'Z',
    18: 'D',
    19: 'B',
    20: 'S',
    21: 'Y',
    22: 'F',
    23: 'X',
    24: 'A',
    25: 'W',
    26: 'J',
    27: '',
    28: 'U',
    29: 'Q',
    30: 'K',
    31: '',
}


def bin2dec(bin):
    dec = 0
    for i, v in enumerate(reversed(bin)):
        dec += (2 ** i) * v

    return dec


def dec2bin(dec):
    bin = []
    v = dec
    while v > 0:
        bin.insert(0, v % 2)
        v //= 2

    return bin


def baudot_char_to_code(char):
    BAUDOT_CODE
    code_dec = next(k for k, v in BAUDOT_CODE.items() if v == char)
    code = dec2bin(code_dec)

    if len(code) < 5:
        code = ([0] * (5 - len(code))) + code

    return code


def baudot_code_to_char(code):
    code_dec = bin2dec(code)
    char = BAUDOT_CODE[code_dec]

    return char


def baudot_str_to_code(s):
    code = []
    for char in s:
        code += baudot_char_to_code(char.upper())

    return code


def baudot_code_to_str(code):
    chars = []
    for i in range(0, len(code), 5):
        chars.append(baudot_code_to_char(code[i : i + 5]))

    s = ''.join(chars)

    return s


def XOR(a, b):
    return int(bool(a) != bool(b))


def XOR_lists(A, B):
    return [XOR(a, b) for a, b in zip(A, B)]


def encrypt(plain_text, key):
    baudot_code = baudot_str_to_code(plain_text)
    cipher_code = XOR_lists(baudot_code, key)

    return cipher_code


def decrypt(cipher_code, key):
    baudot_code = XOR_lists(cipher_code, key)
    plain_text = baudot_code_to_str(baudot_code)

    return plain_text


if __name__ == '__main__':
    message = 'HELLO'
    key = [0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0]

    print('\nMessage:')
    print('--------------------------------------------------')
    print(message)

    print('\nBaudot Code Message:')
    print('--------------------------------------------------')
    print(baudot_str_to_code(message))

    print('\nKey:')
    print('--------------------------------------------------')
    print(key)

    print('\nEncrypted Message:')
    print('--------------------------------------------------')
    cipher_code = encrypt(message, key)
    print(cipher_code)

    print('\nDecrypted Message:')
    print('--------------------------------------------------')
    message_decrypted = decrypt(cipher_code, key)
    print(message_decrypted)
