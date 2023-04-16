import numpy as np


mod_inv = np.vectorize(lambda a, b: pow(int(a), -1, int(b)))


def gcd(a, b):
    if a == 0:
        return b

    if b == 0:
        return a

    return gcd(b, a % b)


def crt(a, m):
    M = np.prod(m)
    Mi = M // m
    y = mod_inv(Mi, m)
    x = np.sum(a * Mi * y) % M

    return x


def square_and_multiply(a, b, n):
    b_bin = np.array([int(i) for i in np.binary_repr(b)])
    l = b_bin.shape[0]
    z = 1

    for i in range(0, l):
        print(z**2, (z ** 2) % n)
        z = (z ** 2) % n

        if b_bin[i] == 1:
            z = (z * a) % n
            print(z)

    return z


if __name__ == '__main__':
    # a = np.array([5, 3, 10])
    # m = np.array([7, 11, 13])
    # print(crt(a, m))
    print(square_and_multiply(5, 37, 47))
