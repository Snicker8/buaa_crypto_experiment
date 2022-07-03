from hashlib import sha256


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


# ECC加法(A + B)
def add(A, B, a, p):
    x1, y1 = A[0], A[1]
    x2, y2 = B[0], B[1]

    if [x1, y1] == [0, 0]:
        return [x2, y2]
    elif [x2, y2] == [0, 0]:
        return [x1, y1]
    elif [x1, y1] == [x2, -y2]:
        return [0, 0]

    if [x1, y1] == [x2, y2]:
        ld = (3 * x1 ** 2 + a) * mr(2 * y1, p)
    else:
        ld = (y2 - y1) * mr(x2 - x1, p)
    x3 = (ld ** 2 - x1 - x2) % p
    y3 = (ld * (x1 - x3) - y1) % p
    return [x3, y3]


# ECC乘法_快速模幂(k * P)
def times(k, P, a, p):
    x1, y1 = P[0], P[1]
    # 计算n的二进制表示
    k_bin = bin(k)[2:]
    [x3, y3] = [0, 0]
    for k_i in k_bin:
        [x3, y3] = add([x3, y3], [x3, y3], a, p)
        if k_i == '1':
            [x3, y3] = add([x3, y3], [x1, y1], a, p)
    return [x3, y3]


# Hash函数_sha256
def hash_256(hex_str):
    return sha256(bytes.fromhex(hex_str)).hexdigest()


# 密钥派生函数KDF
def KDF(Z, klen):
    ct = 1
    Ha = ''
    for i in range(klen // 64):
        Ha += hash_256(Z + hex(ct)[2:].zfill(8))
        ct += 1
    if klen % 64:
        Ha += hash_256(Z + hex(ct)[2:].zfill(8))[:klen % 64]
    return Ha


# SM2加密
def sm2_enc(k, G, P_B, m, a, p, param):
    C1 = times(k, G, a, p)
    C1 = hex(C1[0])[2:].zfill(param) + hex(C1[1])[2:].zfill(param)
    [x2, y2] = times(k, P_B, a, p)
    t = KDF(hex(x2)[2:].zfill(param) + hex(y2)[2:].zfill(param), len(m))
    C2 = hex(int(m, 16) ^ int(t, 16))[2:]
    C3 = hash_256(hex(x2)[2:].zfill(param) + m + hex(y2)[2:].zfill(param))
    return C1 + C2 + C3


def sm2_dec(d, C, a, p, param):
    C1 = [int(C[:param], 16), int(C[param:2 * param], 16)]
    C2 = C[2 * param:-64]
    [x2, y2] = times(d, C1, a, p)
    t = KDF(hex(x2)[2:].zfill(param) + hex(y2)[2:].zfill(param), len(C2))
    m = hex(int(C2, 16) ^ int(t, 16))[2:]
    return m


if __name__ == '__main__':
    p = int(input())
    a = int(input())
    b = int(input())
    G = [int(i) for i in input().split()]
    param = int(input()) // 4
    op = int(input())
    s = input().strip().replace('\n', '').replace('\r', '')[2:]
    if op:
        P_B = [int(i) for i in input().split()]
        k = int(input())
        C = sm2_enc(k, G, P_B, s, a, p, param)
        print('0x04' + C)
    else:
        d = int(input())
        m = sm2_dec(d, s[2:], a, p, param)
        print('0x' + m)
