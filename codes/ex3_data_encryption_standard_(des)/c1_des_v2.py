def h2b(x): return bin(int(x, 16))[2:].zfill(4 * len(x))


def b2h(x): return hex(int(x, 2))[2:].zfill(len(x) // 4)


def xor(x, y): return bin(int(x, 2) ^ int(y, 2))[2:].zfill(len(x))


ip = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

ip_inv = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

pc_1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

pc_2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

e = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

SS = [['1110', '0000', '0100', '1111', '1101', '0111', '0001', '0100', '0010', '1110', '1111', '0010', '1011', '1101',
       '1000', '0001', '0011', '1010', '1010', '0110', '0110', '1100', '1100', '1011', '0101', '1001', '1001', '0101',
       '0000', '0011', '0111', '1000', '0100', '1111', '0001', '1100', '1110', '1000', '1000', '0010', '1101', '0100',
       '0110', '1001', '0010', '0001', '1011', '0111', '1111', '0101', '1100', '1011', '1001', '0011', '0111', '1110',
       '0011', '1010', '1010', '0000', '0101', '0110', '0000', '1101'],
      ['1111', '0011', '0001', '1101', '1000', '0100', '1110', '0111', '0110', '1111', '1011', '0010', '0011', '1000',
       '0100', '1110', '1001', '1100', '0111', '0000', '0010', '0001', '1101', '1010', '1100', '0110', '0000', '1001',
       '0101', '1011', '1010', '0101', '0000', '1101', '1110', '1000', '0111', '1010', '1011', '0001', '1010', '0011',
       '0100', '1111', '1101', '0100', '0001', '0010', '0101', '1011', '1000', '0110', '1100', '0111', '0110', '1100',
       '1001', '0000', '0011', '0101', '0010', '1110', '1111', '1001'],
      ['1010', '1101', '0000', '0111', '1001', '0000', '1110', '1001', '0110', '0011', '0011', '0100', '1111', '0110',
       '0101', '1010', '0001', '0010', '1101', '1000', '1100', '0101', '0111', '1110', '1011', '1100', '0100', '1011',
       '0010', '1111', '1000', '0001', '1101', '0001', '0110', '1010', '0100', '1101', '1001', '0000', '1000', '0110',
       '1111', '1001', '0011', '1000', '0000', '0111', '1011', '0100', '0001', '1111', '0010', '1110', '1100', '0011',
       '0101', '1011', '1010', '0101', '1110', '0010', '0111', '1100'],
      ['0111', '1101', '1101', '1000', '1110', '1011', '0011', '0101', '0000', '0110', '0110', '1111', '1001', '0000',
       '1010', '0011', '0001', '0100', '0010', '0111', '1000', '0010', '0101', '1100', '1011', '0001', '1100', '1010',
       '0100', '1110', '1111', '1001', '1010', '0011', '0110', '1111', '1001', '0000', '0000', '0110', '1100', '1010',
       '1011', '0001', '0111', '1101', '1101', '1000', '1111', '1001', '0001', '0100', '0011', '0101', '1110', '1011',
       '0101', '1100', '0010', '0111', '1000', '0010', '0100', '1110'],
      ['0010', '1110', '1100', '1011', '0100', '0010', '0001', '1100', '0111', '0100', '1010', '0111', '1011', '1101',
       '0110', '0001', '1000', '0101', '0101', '0000', '0011', '1111', '1111', '1010', '1101', '0011', '0000', '1001',
       '1110', '1000', '1001', '0110', '0100', '1011', '0010', '1000', '0001', '1100', '1011', '0111', '1010', '0001',
       '1101', '1110', '0111', '0010', '1000', '1101', '1111', '0110', '1001', '1111', '1100', '0000', '0101', '1001',
       '0110', '1010', '0011', '0100', '0000', '0101', '1110', '0011'],
      ['1100', '1010', '0001', '1111', '1010', '0100', '1111', '0010', '1001', '0111', '0010', '1100', '0110', '1001',
       '1000', '0101', '0000', '0110', '1101', '0001', '0011', '1101', '0100', '1110', '1110', '0000', '0111', '1011',
       '0101', '0011', '1011', '1000', '1001', '0100', '1110', '0011', '1111', '0010', '0101', '1100', '0010', '1001',
       '1000', '0101', '1100', '1111', '0011', '1010', '0111', '1011', '0000', '1110', '0100', '0001', '1010', '0111',
       '0001', '0110', '1101', '0000', '1011', '1000', '0110', '1101'],
      ['0100', '1101', '1011', '0000', '0010', '1011', '1110', '0111', '1111', '0100', '0000', '1001', '1000', '0001',
       '1101', '1010', '0011', '1110', '1100', '0011', '1001', '0101', '0111', '1100', '0101', '0010', '1010', '1111',
       '0110', '1000', '0001', '0110', '0001', '0110', '0100', '1011', '1011', '1101', '1101', '1000', '1100', '0001',
       '0011', '0100', '0111', '1010', '1110', '0111', '1010', '1001', '1111', '0101', '0110', '0000', '1000', '1111',
       '0000', '1110', '0101', '0010', '1001', '0011', '0010', '1100'],
      ['1101', '0001', '0010', '1111', '1000', '1101', '0100', '1000', '0110', '1010', '1111', '0011', '1011', '0111',
       '0001', '0100', '1010', '1100', '1001', '0101', '0011', '0110', '1110', '1011', '0101', '0000', '0000', '1110',
       '1100', '1001', '0111', '0010', '0111', '0010', '1011', '0001', '0100', '1110', '0001', '0111', '1001', '0100',
       '1100', '1010', '1110', '1000', '0010', '1101', '0000', '1111', '0110', '1100', '1010', '1001', '1101', '0000',
       '1111', '0011', '0011', '0101', '0101', '0110', '1000', '1011']]

p = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]


def IP(m):
    m_ip = ''
    for i in range(64): m_ip += (m[ip[i] - 1])
    return m_ip


def IP_inv(m):
    m_ip_inv = ''
    for i in range(64): m_ip_inv += (m[ip_inv[i] - 1])
    return m_ip_inv


def PC_1(k):
    k_pc_1 = ''
    for i in range(56): k_pc_1 += k[pc_1[i] - 1]
    return k_pc_1


def PC_2(k):
    k_pc_2 = ''
    for i in range(48): k_pc_2 += k[pc_2[i] - 1]
    return k_pc_2


def LS(s, i):
    ls = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    s = s[ls[i]:] + s[:ls[i]]
    return s


def key_gen(k):
    k = PC_1(k)
    C, D = k[:28], k[28:]
    K = []
    for i in range(16):
        C, D = LS(C, i), LS(D, i)
        K.append(PC_2(C + D))
    return K


def E(s):
    s_e = ''
    for i in range(48): s_e += s[e[i] - 1]
    return s_e


def S(R):
    Rs = []
    for i in range(8): Rs.append(R[6 * i: 6 * (i + 1)])
    for i in range(8):
        Rs[i] = SS[i][int(Rs[i], 2)]
    R = ''
    for i in range(8): R += Rs[i]
    return R


def P(s):
    s_p = ''
    for i in range(32): s_p += s[p[i] - 1]
    return s_p


def f(R, k): return P(S(xor(E(R), k)))


def DES_enc(m, k):
    m = h2b(m)
    k = h2b(k)
    m = IP(m)
    L, R = m[:32], m[32:]
    K = key_gen(k)
    for i in range(16):
        L, R = R, xor(L, f(R, K[i]))
        m = L + R
    m = IP_inv(m[32:] + m[:32])
    return b2h(m)


def DES_dec(c, k):
    c = h2b(c)
    k = h2b(k)
    c = IP(c)
    R, L = c[:32], c[32:]
    K = key_gen(k)
    for i in range(15, -1, -1):
        R_i = R
        R = L
        L = xor(R_i, f(R, K[i]))
        c = L + R
    c = IP_inv(c)
    return b2h(c)


if __name__ == "__main__":
    T = int(input())
    s = input().strip().replace('\n', '').replace('\r', '')[2:]
    k = input().strip().replace('\n', '').replace('\r', '')[2:]
    op = int(input())
    for i in range(T):
        s = DES_enc(s, k) if op else DES_dec(s, k)
    print('0x' + s)
