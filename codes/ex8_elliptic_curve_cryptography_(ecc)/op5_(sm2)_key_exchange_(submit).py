from hashlib import sha256
from math import log2, ceil


# 求gcd
def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b


# 求模逆
def mr(x, p):
    x %= p
    if gcd(x, p) != 1:
        return None
    u1, u2, u3 = 1, 0, x
    v1, v2, v3 = 0, 1, p
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % p


# 转字节串
def tb(x):
    global param
    if isinstance(x, int):
        return int(x).to_bytes(param // 8, 'big')
    elif isinstance(x, str):
        return int(x, 16).to_bytes(len(x) // 2, 'big')
    return False


# 椭圆曲线类
class ECC():
    # ECC参数：大素数p，系数a,b，基点G，G的阶n
    def __init__(self, p, a, b, G, n):
        self.p = p
        self.a = a
        self.b = b
        self.G = G
        self.n = n

    # 判断是否在曲线上
    def on_curve(self, x, y):
        return (y * y) % self.p == (x ** 3 + self.a * x + self.b) % self.p

    # ECC上点加
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

    # ECC乘法_快速模幂(k * P)
    def times(self, k, P):
        x1, y1 = P[0], P[1]
        # 计算n的二进制表示
        k_bin = bin(k)[2:]
        [x3, y3] = [0, 0]
        for k_i in k_bin:
            [x3, y3] = self.add([x3, y3], [x3, y3])
            if k_i == '1':
                [x3, y3] = self.add([x3, y3], [x1, y1])
        return [x3, y3]


# 密钥派生函数KDF
def KDF(Z, klen):
    T = ''
    k = (klen + 31) // 32
    for counter in range(1, k + 1):
        cnt = counter.to_bytes(4, 'big')
        T += sha256(Z + cnt).hexdigest()
    return T[:2 * klen]


if __name__ == '__main__':
    h = 1
    param = 256
    klen = 128
    part = input()
    p = int(input())
    a = int(input())
    b = int(input())
    G = [int(i) for i in input().split()]
    n = int(input())
    ecc = ECC(p, a, b, G, n)

    id_A = input().strip().replace('\n', '').replace('\r', '')
    id_B = input().strip().replace('\n', '').replace('\r', '')
    d_self = int(input())
    P_A = [int(i) for i in input().split()]
    P_B = [int(i) for i in input().split()]
    r_self = int(input())
    R_other = [int(i) for i in input().split()]

    w = ceil(ceil(log2(n)) // 2) - 1
    entl_A = int(4 * len(id_A)).to_bytes(2, 'big')
    entl_B = int(4 * len(id_B)).to_bytes(2, 'big')
    Z_A = tb(sha256(entl_A + tb(id_A) + tb(a) + tb(b) + tb(G[0]) + tb(G[1]) + tb(P_A[0]) + tb(P_A[1])).hexdigest())
    Z_B = tb(sha256(entl_B + tb(id_B) + tb(a) + tb(b) + tb(G[0]) + tb(G[1]) + tb(P_B[0]) + tb(P_B[1])).hexdigest())

    if part == 'A':
        R_self = ecc.times(r_self, G)
        x1, y1 = R_self
        x1_ = (1 << w) + (x1 & ((1 << w) - 1))
        t_self = (d_self + x1_ * r_self) % n
        x2, y2 = R_other
        x2_ = (1 << w) + (x2 & ((1 << w) - 1))
        U = ecc.times(h * t_self, ecc.add(P_B, ecc.times(x2_, R_other)))
        x_U, y_U = tb(U[0]), tb(U[1])
        K_A = KDF(x_U + y_U + Z_A + Z_B, klen // 8)
        S_1 = sha256(b'\x02' + y_U + sha256(x_U + Z_A + Z_B + tb(x1) + tb(y1) + tb(x2) + tb(y2)).digest()).hexdigest()
        S_A = sha256(b'\x03' + y_U + sha256(x_U + Z_A + Z_B + tb(x1) + tb(y1) + tb(x2) + tb(y2)).digest()).hexdigest()
        print(int(K_A, 16))
        print(int(S_1, 16), int(S_A, 16))
    else:
        R_self = ecc.times(r_self, G)
        x2, y2 = R_self
        x2_ = (1 << w) + (x2 & ((1 << w) - 1))
        t_self = (d_self + x2_ * r_self) % n
        x1, y1 = R_other
        x1_ = (1 << w) + (x1 & ((1 << w) - 1))
        V = ecc.times(h * t_self, ecc.add(P_A, ecc.times(x1_, R_other)))
        x_V, y_V = tb(V[0]), tb(V[1])
        K_B = KDF(x_V + y_V + Z_A + Z_B, klen // 8)
        S_B = sha256(b'\x02' + y_V + sha256(x_V + Z_A + Z_B + tb(x1) + tb(y1) + tb(x2) + tb(y2)).digest()).hexdigest()
        S_2 = sha256(b'\x03' + y_V + sha256(x_V + Z_A + Z_B + tb(x1) + tb(y1) + tb(x2) + tb(y2)).digest()).hexdigest()
        print(int(K_B, 16))
        print(int(S_B, 16), int(S_2, 16))
