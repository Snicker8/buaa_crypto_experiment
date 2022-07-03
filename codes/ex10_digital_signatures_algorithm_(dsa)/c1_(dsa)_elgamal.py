from hashlib import sha256


def mr(x, p):
    '''
    :return: x ^ -1 mod p
    '''
    x %= p
    u1, u2, u3 = 1, 0, x
    v1, v2, v3 = 0, 1, p
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % p


class DS_ElGamal():
    def __init__(self, q, alpha):
        self.q = q
        self.alpha = alpha

    def sign(self, m, X_A, K):
        m = int(sha256(m).hexdigest(), 16)
        S1 = pow(self.alpha, K, self.q)
        K_ = mr(K, self.q - 1)
        S2 = K_ * (m - X_A * S1) % (self.q - 1)
        return S1, S2

    def verify(self, m, Y_A, S1, S2):
        m = int(sha256(m).hexdigest(), 16)
        V1 = pow(self.alpha, m, self.q)
        V2 = pow(Y_A, S1, self.q) * pow(S1, S2, self.q) % self.q
        return V1 == V2


def main():
    q = int(input())
    alpha = int(input())
    m = input().encode('utf-8')
    mode = input()
    ds = DS_ElGamal(q, alpha)
    if mode == 'Sign':
        X_A = int(input())
        K = int(input())
        S1, S2 = ds.sign(m, X_A, K)
        print(S1, S2)
    else:
        Y_A = int(input())
        S1, S2 = map(int, input().split())
        print(ds.verify(m, Y_A, S1, S2))


if __name__ == '__main__':
    main()
