import string
import re
from collections import Counter

with open('data/excerpt.txt', 'r') as excerpt_file:
    EXCERPT = re.sub('\s+', ' ', excerpt_file.read())

def encrypt(plain_text, key):
    cipher_text = ''
    for c in plain_text:
        if c.isalpha():
            offset = ord('a') if c.islower() else ord('A')
            cipher_text += chr(((ord(c) - offset + key) % 25) + offset)
        else:
            cipher_text += c

    return cipher_text

def decrypt(cipher_text, key):
    plain_text = ''
    for c in cipher_text:
        if c.isalpha():
            offset = ord('a') if c.islower() else ord('A')
            plain_text += chr(((ord(c) - offset - key) % 25) + offset)
        else:
            plain_text += c

    return plain_text

def brute_force(cipher_text):
    plain_texts = []

    for key in range(26):
        plain_texts.append(decrypt(cipher_text, key))

    return plain_texts

def get_letter_freq(text):
    letter_count = Counter([c.lower() for c in text if c.isalpha()])
    alpha_len = sum(letter_count.values())
    letter_freq = {k : v / alpha_len for k, v in letter_count.items()}

    return letter_freq

def mean_squared_error_alpha(freq1, freq2):
    mse = 0
    for a in string.ascii_lowercase:
        mse += (freq1.get(a, 0.0) - freq2.get(a, 0.0)) ** 2

    return mse

def decipher(cipher_text, best_match=False):
    excerpt_letter_freq = get_letter_freq(EXCERPT)
    plain_texts = brute_force(cipher_text)
    plain_text_mse = []

    for plain_text in plain_texts:
        letter_freq = get_letter_freq(plain_text)
        mse = mean_squared_error_alpha(excerpt_letter_freq, letter_freq)
        if len(plain_text_mse) < 1 or not best_match:
            plain_text_mse.append([plain_text, mse])
        else:
            if mse < plain_text_mse[0][1]:
                plain_text_mse[0][0] = plain_text
                plain_text_mse[0][1] = mse

    return plain_text_mse

if __name__ == '__main__':
    with open('data/message.txt', 'r') as message_file:
        message = re.sub('\s+', ' ', message_file.read())

    key = 12

    print('\nMessage:')
    print('--------------------------------------------------')
    print(message)

    print('\nEncrypted Message:')
    print('--------------------------------------------------')
    cipher_text = encrypt(message, key)
    print(cipher_text)

    print('\nDecrypted Message:')
    print('--------------------------------------------------')
    message_decrypted = decrypt(cipher_text, key)
    print(message_decrypted)

    print('\nDeciphered Message (Without Key):')
    print('--------------------------------------------------')
    message_deciphered = decipher(cipher_text, best_match=True)[0][0]
    print(message_deciphered)
