T = [0x79cc4519] * 16 + [0x7a879d8a] * 48


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
def hash_sm3(msg):
    msg, group_len = padding(msg)
    B = gourping(msg, group_len)
    V = [0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e]
    for i in range(group_len):
        V = CF(V, B[i])
    return hex(
        ((((((V[0] << 32 | V[1]) << 32 | V[2]) << 32 | V[3]) << 32 | V[4]) << 32 | V[5]) << 32 | V[6]) << 32 | V[7])[
           2:].zfill(64)


if __name__ == '__main__':
    msg = input().encode()
    print(hash_sm3(msg))
