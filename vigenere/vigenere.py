import string
import re
from collections import Counter

with open('excerpt.txt', 'r') as excerpt_file:
    excerpt = re.sub('\s+', ' ', excerpt_file.read())

def clean_non_alpha(text):
    clean_text = ''.join(re.findall('[a-zA-Z]+', text))

    return clean_text

def encrypt(plain_text, key):
    cipher_text = ''
    clean_plain_text = clean_non_alpha(plain_text).lower()
    clean_key = clean_non_alpha(key).lower()

    for i, c in enumerate(clean_plain_text):
        letter_idx = ord(c) - ord('a')
        key_idx = ord(clean_key[i % len(clean_key)]) - ord('a')
        cipher_text += chr(((letter_idx + key_idx) % 25) + ord('a'))

    return cipher_text

def decrypt_single_key(cipher_text, key):
    plain_text = ''
    clean_cipher_text = clean_non_alpha(cipher_text).lower()

    for c in clean_cipher_text:
        offset = ord('a') if c.islower() else ord('A')
        plain_text += chr(((ord(c) - offset - key) % 25) + offset)

    return plain_text

def decrypt(cipher_text, key):
    plain_text = ''
    clean_cipher_text = clean_non_alpha(cipher_text).lower()
    clean_key = clean_non_alpha(key).lower()

    for i, c in enumerate(clean_cipher_text):
        letter_idx = ord(c) - ord('a')
        key_idx = ord(clean_key[i % len(clean_key)]) - ord('a')
        plain_text += chr(((letter_idx - key_idx) % 25) + ord('a'))

    return plain_text

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

def brute_force(text):
    plain_texts = []

    for key in range(26):
        plain_texts.append(decrypt_single_key(text, key))

    return plain_texts

def decipher_subset(text):
    excerpt_letter_freq = get_letter_freq(excerpt)
    plain_texts = brute_force(text)
    min_mse_plain_text = ''
    min_mse = -1

    for plain_text in plain_texts:
        letter_freq = get_letter_freq(plain_text)
        mse = mean_squared_error_alpha(excerpt_letter_freq, letter_freq)
        if min_mse < 0 or mse < min_mse:
            min_mse_plain_text = plain_text
            min_mse = mse

    return min_mse_plain_text

def decipher(cipher_text, key_len_range):
    plain_texts = []
    for key_len in range(*key_len_range):
        plain_text = [''] * len(cipher_text)
        for offset in range(key_len):
            subset_text = ''.join([
                c for i, c in enumerate(cipher_text)
                if (i - offset) % key_len == 0
            ])
            plain_subset_text = decipher_subset(subset_text)

            j = 0
            for i in range(len(plain_text)):
                if (i - offset) % key_len == 0:
                    plain_text[i] = plain_subset_text[j]
                    j += 1

        plain_texts.append(''.join(plain_text))

    return plain_texts

if __name__ == '__main__':
    with open('message.txt', 'r') as message_file:
        message = re.sub('\s+', ' ', message_file.read())
    # message = 'hellohowareyoumaniamdoingverywelltobehonestthisisthebiggestmaddestgigihaveeverhadthepleasureofdoing'

    with open('key.txt', 'r') as key_file:
        key = re.sub('\s+', ' ', key_file.read())

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
    key_len_range = (6, 7)
    message_deciphered = decipher(cipher_text, key_len_range)
    for m in message_deciphered:
        print(m)
