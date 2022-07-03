class RSA:
    def __init__(self, p, q, e):
        self.p = p
        self.q = q
        self.n = p * q
        self.e = e

    @staticmethod
    def fastpow(x, k, m):
        a = 1
        while k:
            if k & 1:
                a = a * x % m
            k = k >> 1
            x = x * x % m
        return a

    @staticmethod
    def gcd_expand(a1, a2):
        if a2 == 0:
            return a1, 1, 0
        elif a1 == 0:
            return a2, 0, 1
        else:
            GCD, xtmp, ytmp = RSA.gcd_expand(a2, a1 % a2)
            x = ytmp
            y = xtmp - ytmp * (a1 // a2)
            return GCD, x, y

    @staticmethod
    def invert(x, m):
        g, x_, y_ = RSA.gcd_expand(x, m)
        return x_ % m

    def encrypt(self, m):
        return self.fastpow(m, self.e, self.n)

    def decrypt(self, m):
        # phi(n)
        phi = (self.p - 1) * (self.q - 1)
        # d是e模phi的逆元
        d = RSA.invert(self.e, phi)
        return self.fastpow(m, d, self.n)


def main():
    p = int(input())
    q = int(input())
    e = int(input())
    m = int(input())
    mode = int(input())
    rsa = RSA(p=p, q=q, e=e)
    if mode:
        print(rsa.encrypt(m=m))
    else:
        print(rsa.decrypt(m=m))


if __name__ == "__main__":
    main()
