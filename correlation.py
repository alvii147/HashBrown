import numpy as np


def auto_correlation(a, tau_range):
    corr = cross_correlation(a, a, tau_range)

    return corr


def cross_correlation(a, b, tau_range):
    if a.shape[0] < b.shape[0]:
        a, b = b, a

    corr = np.zeros(tau_range[1] - tau_range[0], dtype=int)
    for i, tau in enumerate(range(*tau_range)):
        corr[i] = np.sum(
            np.where(
                (a + np.resize(b, a.shape[0] + tau)[tau:]) % 2 == 0,
                1,
                -1,
            )
        )

    return corr


if __name__ == '__main__':
    a = np.array([1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1], dtype=int)
    b = np.array([1, 1, 1, 0, 0], dtype=int)
    print(cross_correlation(a, b, (1, 4)))
