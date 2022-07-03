# 求模逆
def mr(x, p):
    x %= p
    u1, u2, u3 = 1, 0, x
    v1, v2, v3 = 0, 1, p
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % p


# 计算整数k的NAF形式
def naf(k):
    i = 0
    k_list = []
    while k > 0:
        if k & 1:
            ki = 2 - (k & 0b11)
            k = k - ki
        else:
            ki = 0
        k_list.append(ki)
        k = k >> 1
        i = i + 1
    return k_list


class ECC():
    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b

    # ECC加法(A + B)
    def add(self, A, B):
        x1, y1 = A[0], A[1]
        x2, y2 = B[0], B[1]
        if [x1, y1] == [0, 0]:
            return [x2, y2]
        elif [x2, y2] == [0, 0]:
            return [x1, y1]
        elif [x1, y1] == [x2, -y2]:
            return [0, 0]
        if [x1, y1] == [x2, y2]:
            ld = (3 * x1 ** 2 + self.a) * mr(2 * y1, self.p)
        else:
            ld = (y2 - y1) * mr(x2 - x1, self.p)
        x3 = (ld ** 2 - x1 - x2) % self.p
        y3 = (ld * (x1 - x3) - y1) % self.p
        return [x3, y3]

    # ECC乘法_快速模幂plus版(k * P)
    def times(self, k, P):
        # 计算k的naf表示
        k_naf = naf(k)
        x1, y1 = P
        res = [0, 0]
        for k_i in k_naf:
            if k_i == 1:
                res = self.add(res, [x1, y1])
            elif k_i == -1:
                res = self.add(res, [x1, -y1])
            [x1, y1] = self.add([x1, y1], [x1, y1])
        return res


def main():
    p = int(input())
    a = int(input())
    b = int(input())
    ecc = ECC(p, a, b)
    P = [int(i) for i in input().split()]
    op = int(input())
    if op:
        M = [int(i) for i in input().split()]
        r = int(input())
        Q = [int(i) for i in input().split()]
        N = int(input())
        C1 = ecc.times(r, P)
        C2 = ecc.add(M, ecc.times(r * (N + 1), Q))
        print(" ".join(str(i) for i in C1))
        print(" ".join(str(i) for i in C2))
    else:
        C1 = [int(i) for i in input().split()]
        C2 = [int(i) for i in input().split()]
        k = int(input())
        N = int(input())
        temp = ecc.times(N + 1, ecc.times(k, C1))
        temp[1] = -temp[1]
        M = ecc.add(C2, temp)
        print(" ".join(str(i) for i in M))


if __name__ == '__main__':
    main()
