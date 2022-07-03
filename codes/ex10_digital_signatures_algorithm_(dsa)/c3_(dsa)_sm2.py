T = [0x79cc4519] * 16 + [0x7a879d8a] * 48


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


# ECC乘法的优化实现中使用
def naf(k):
    '''
    :return: k的NAF表示
    '''
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


# 32比特数循环左移k位
def shift_32(n_32bit, k):
    return ((n_32bit << k) | (n_32bit >> (32 - k))) & 0xffffffff


# 置换函数——P_0
def P_0(X):
    return X ^ shift_32(X, 9) ^ shift_32(X, 17)


# 置换函数——P_1
def P_1(X):
    return X ^ shift_32(X, 15) ^ shift_32(X, 23)


# 布尔函数FF_j
def FF(j, X, Y, Z):
    if j <= 15:
        return X ^ Y ^ Z
    else:
        return (X & Y) | (X & Z) | (Y & Z)


# 布尔函数GG_j
def GG(j, X, Y, Z):
    if j <= 15:
        return X ^ Y ^ Z
    else:
        return (X & Y) | ((X ^ 0xffffffff) & Z)


# SM3初始化——填充（同SHA1）
def padding(msg):
    msg_bitlen = len(msg) * 8
    int_msg = int.from_bytes(msg, 'big')
    int_msg = ((int_msg << 1) | 1) << (512 - (msg_bitlen + 64) % 512) - 1
    int_msg = int_msg << 64 | msg_bitlen
    return int_msg, (msg_bitlen + 64) // 512 + 1


# 报文分组
def gourping(msg, group_len):
    msg_groups = []
    for _ in range(group_len):
        msg_groups.append(msg & ((1 << 512) - 1))
        msg >>= 512
    return msg_groups[::-1]


# 压缩函数——CF
def CF(V_i, B_i):
    W, W_ = [], []
    for i in range(16):
        W.append(B_i & 0xffffffff)
        B_i >>= 32
    W = W[::-1]
    for i in range(16, 68):
        W.append(P_1(W[i - 16] ^ W[i - 9] ^ shift_32(W[i - 3], 15)) ^ shift_32(W[i - 13], 7) ^ W[i - 6])
    for i in range(64):
        W_.append(W[i] ^ W[i + 4])

    A, B, C, D, E, F, G, H = V_i
    for i in range(64):
        SS1 = shift_32((shift_32(A, 12) + E + shift_32(T[i], i % 32)) % (1 << 32), 7)
        SS2 = SS1 ^ shift_32(A, 12)
        TT1 = (FF(i, A, B, C) + D + SS2 + W_[i]) % (1 << 32)
        TT2 = (GG(i, E, F, G) + H + SS1 + W[i]) % (1 << 32)
        D = C
        C = shift_32(B, 9)
        B = A
        A = TT1
        H = G
        G = shift_32(F, 19)
        F = E
        E = P_0(TT2)
    V_i = [(V_i[0] ^ A) & 0xffffffff, (V_i[1] ^ B) & 0xffffffff, (V_i[2] ^ C) & 0xffffffff,
           (V_i[3] ^ D) & 0xffffffff, (V_i[4] ^ E) & 0xffffffff, (V_i[5] ^ F) & 0xffffffff, (V_i[6] ^ G) & 0xffffffff,
           (V_i[7] ^ H) & 0xffffffff]
    return V_i


# 国密算法——SM3
def H(msg):
    msg, group_len = padding(msg)
    B = gourping(msg, group_len)
    V = [0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e]
    for i in range(group_len):
        V = CF(V, B[i])
    return hex(
        ((((((V[0] << 32 | V[1]) << 32 | V[2]) << 32 | V[3]) << 32 | V[4]) << 32 | V[5]) << 32 | V[6]) << 32 | V[7])[
           2:].zfill(64)


# 椭圆曲线类：加法、乘法
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


# 求用户A的参数Z_A = H(ENTL_A||ID_A||a||b||x_G||y_G||x_A||y_A)
def get_Z_A(ID_A, P_A):
    global a, b, G
    ENTL_A = hex(len(ID_A.encode() * 8))[2:].zfill(4)
    ID_A = ID_A.encode().hex()
    temp = ENTL_A + ID_A
    for int_number in a, b, G[0], G[1], P_A[0], P_A[1]:
        temp += hex(int_number)[2:].zfill(64)
    Z_A = H(bytes.fromhex(temp))
    return Z_A


# SM2签名算法
def sign(ID_A, P_A, M, d_A, k):
    global p, a, b, G, n
    ecc = ECC(p, a, b)
    Z_A = get_Z_A(ID_A, P_A)
    M = M.encode().hex()
    # e = H(Z_A||M)
    e = int(H(bytes.fromhex(Z_A + M)), 16)
    x1, y1 = ecc.times(k, G)
    r = (e + x1) % n
    s = (mr(1 + d_A, n) * (k - r * d_A)) % n
    return r, s


# SM2验证算法
def verify(ID_A, P_A, M, r, s):
    global p, a, b, G, n
    ecc = ECC(p, a, b)
    Z_A = get_Z_A(ID_A, P_A)
    M = M.encode().hex()
    e = int(H(bytes.fromhex(Z_A + M)), 16)
    t = (r + s) % n
    x1, y1 = ecc.add(ecc.times(s, G), ecc.times(t, P_A))
    R = (e + x1) % n
    return R == r


def main():
    global p, a, b, G, n
    p = int(input())
    a = int(input())
    b = int(input())
    G = [int(i) for i in input().split()]
    n = int(input())
    ID_A = input()
    P_A = [int(i) for i in input().split()]
    M = input()
    mode = input()
    if mode == 'Sign':
        d_A = int(input())
        k = int(input())
        r, s = sign(ID_A, P_A, M, d_A, k)
        print(r)
        print(s)
    else:
        r = int(input())
        s = int(input())
        print(verify(ID_A, P_A, M, r, s))


if __name__ == '__main__':
    main()
