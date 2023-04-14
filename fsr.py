import numpy as np


class FSR:
    def __init__(self, initial_state, f):
        self.state = np.array(initial_state, dtype=int)
        self.f = f
        self.n = self.state.shape[0]

    def __iter__(self):
        return self

    def __next__(self):
        self.state = np.concatenate((self.state, [self.f(*self.state[-self.n:])]))

        return self.state

    def __str__(self):
        return ''.join(self.state.astype(str))

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    f = lambda x0, x1, x2: np.logical_xor(x0, x1)
    fsr = FSR([0, 1, 0], f)
    for state in fsr:
        print(fsr)
        if 'q' in input():
            break
