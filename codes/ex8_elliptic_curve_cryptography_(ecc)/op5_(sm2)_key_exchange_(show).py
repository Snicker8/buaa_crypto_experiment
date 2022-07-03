from random import randint
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
    def on_curve(self, A):
        x, y = A
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


def main():
    global h, param, klen
    h = 1
    param = 256
    klen = 128

    # 输入的基本参数
    p = int(input())
    a = int(input())
    b = int(input())
    G = [int(i) for i in input().split()]
    n = int(input())
    ecc = ECC(p, a, b, G, n)

    # 算ECC系统参数
    id_A = input().strip().replace('\n', '').replace('\r', '')
    id_B = input().strip().replace('\n', '').replace('\r', '')
    d_A = randint(1, n - 2)
    d_B = randint(1, n - 2)
    P_A = ecc.times(d_A, G)
    P_B = ecc.times(d_B, G)
    w = ceil(ceil(log2(n)) // 2) - 1
    entl_A = int(4 * len(id_A)).to_bytes(2, 'big')
    entl_B = int(4 * len(id_B)).to_bytes(2, 'big')
    Z_A = tb(sha256(entl_A + tb(id_A) + tb(a) + tb(b) + tb(G[0]) + tb(G[1]) + tb(P_A[0]) + tb(P_A[1])).hexdigest())
    Z_B = tb(sha256(entl_B + tb(id_B) + tb(a) + tb(b) + tb(G[0]) + tb(G[1]) + tb(P_B[0]) + tb(P_B[1])).hexdigest())

    # 按顺序执行协议
    print('A进行第1步到第5步的计算：r_A,R_A,x_1_,t_A')
    r_A = randint(1, n - 1)
    R_A = ecc.times(r_A, G)
    print('A将R_A发送给B')
    x1, y1 = R_A
    x1_ = (1 << w) + (x1 & ((1 << w) - 1))
    t_A = (d_A + x1_ * r_A) % n
    print()

    print('B进行第1步到第4步的计算：r_B,R_B,x2_,t_B')
    r_B = randint(1, n - 1)
    R_B = ecc.times(r_B, G)
    x2, y2 = R_B
    x2_ = (1 << w) + (x2 & ((1 << w) - 1))
    t_B = (d_B + x2_ * r_B) % n
    print('B收到R_A，对其进行检验:')
    if ecc.on_curve(R_A) is False:
        print('B协商失败！！！')
        exit(1)
    else:
        print('检验通过！！！')
    print()

    print('B进行第5步到第6步计算：x1_,V')
    x1, y1 = R_A
    x1_ = (1 << w) + (x1 & ((1 << w) - 1))
    V = ecc.times(h * t_B, ecc.add(P_A, ecc.times(x1_, R_A)))
    print('B对V进行检验')
    if V == [0, 0]:
        print('B协商失败！！！')
        exit(1)
    else:
        print('检验通过！！！')
    print()

    print('B进行第7步到第10步计算')
    x_V, y_V = tb(V[0]), tb(V[1])
    K_B = KDF(x_V + y_V + Z_A + Z_B, klen // 8)
    S_B = sha256(b'\x02' + y_V + sha256(x_V + Z_A + Z_B + tb(x1) + tb(y1) + tb(x2) + tb(y2)).digest()).hexdigest()
    S_2 = sha256(b'\x03' + y_V + sha256(x_V + Z_A + Z_B + tb(x1) + tb(y1) + tb(x2) + tb(y2)).digest()).hexdigest()
    print('K_B:', int(K_B, 16))
    print('S_B:', int(S_B, 16))
    print('B将R_B与S_B发送给A')
    print('S_2:', int(S_2, 16))
    print()

    print('A收到R_B，对其进行检验')
    if ecc.on_curve(R_B) is False:
        print('A协商失败！！！')
        exit(1)
    else:
        print('检验通过！！！')
    print()

    print('A进行第6步到第7步计算：x2_,U')
    x2, y2 = R_B
    x2_ = (1 << w) + (x2 & ((1 << w) - 1))
    U = ecc.times(h * t_A, ecc.add(P_B, ecc.times(x2_, R_B)))
    print('A对U进行检验')
    if U == [0, 0]:
        print('A协商失败！！！')
        exit(1)
    else:
        print('检验通过！！！')
    print()

    print('A进行第8步到第9步计算：K_A,S_1')
    x_U, y_U = tb(U[0]), tb(U[1])
    K_A = KDF(x_U + y_U + Z_A + Z_B, klen // 8)
    S_1 = sha256(b'\x02' + y_U + sha256(x_U + Z_A + Z_B + tb(x1) + tb(y1) + tb(x2) + tb(y2)).digest()).hexdigest()
    print('K_A:', int(K_A, 16))
    print('S_1:', int(S_1, 16))
    print('A检验S1与S_B是否相等')
    if S_1 == S_B:
        print('S_1 = S_B！！！')
    else:
        print('A协商失败！！！')
        exit(1)
    print()

    print('A进行第10步计算')
    S_A = sha256(b'\x03' + y_U + sha256(x_U + Z_A + Z_B + tb(x1) + tb(y1) + tb(x2) + tb(y2)).digest()).hexdigest()
    print('S_A:', int(S_A, 16))
    print('B检验S2与S_A是否相等')
    if S_2 == S_A:
        print('S_2 = S_A！！！')
    else:
        print('B协商失败！！！')
        exit(1)

    print('协商成功！！！')
    print('协商密钥为:', int(K_A, 16))
    exit(0)


if __name__ == '__main__':
    main()
