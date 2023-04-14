import numpy as np


def KSA(K, N):
    S = np.arange(N)

    for i in range(N):
        j = (j + S[i] + K[i % K.shape[0]]) % N
        S[i], S[j] = S[j], S[i]

    return S

def PRGA(S, plaintext_length):
    N = S.shape[0]
    z = np.zeros(plaintext_length, dtype=int)
    i, j = 0, 0

    for n in range(plaintext_length):
        i = (i + 1) % N
        j = (j + S[i]) % N

        S[i], S[j] = S[j], S[i]
        z[n] = S[(S[i] + S[j]) % N]

    return z


if __name__ == '__main__':
    S = np.zeros(256, dtype=int)
    S[0], S[1] = 1, 2
    print(PRGA(S, 10))
