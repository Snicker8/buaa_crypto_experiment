def h2b(x): return bin(int(x, 16))[2:].zfill(4 * len(x))


def b2h(x): return hex(int(x, 2))[2:].zfill(len(x) // 4)


def print_matrix(a):
    for i in range(16):
        for j in range(16):
            print('0x' + a[i][j], end=' ')
        print()


def multiply(a1, a2):
    res = 0
    poly = int('100011011', 2)
    digit_1 = poly.bit_length() - 1
    while a2:
        if a2 & 1:
            res = res ^ a1
        a1, a2 = a1 << 1, a2 >> 1
        if a1 >> digit_1:
            a1 = a1 ^ poly
    return res


def divide(a1, a2):
    len1, len2 = a1.bit_length(), a2.bit_length()
    len = len1 - len2 + 1
    if len < 1: return 0, a1
    div = 0
    while len1 >= len2:
        a1 ^= (a2 << (len1 - len2))
        div ^= (1 << (len1 - len2))
        len1 = a1.bit_length()
    return div, a1


def inverse(a):
    a = int(a, 16)
    b = int('100011011', 2)
    x1, y1, x2, y2 = 1, 0, 0, 1
    while b:
        q, r = divide(a, b)
        a, b = b, r
        x1, x2 = x2, x1 ^ multiply(q, x2)
        y1, y2 = y2, y1 ^ multiply(q, y2)
    return hex(x1)[2:].zfill(2)


# 初始化
def init(S_box):
    for i in range(16):
        for j in range(16):
            S_box[i][j] = hex(i)[2:] + hex(j)[2:]


# 逐字节求逆元
def inverse_matrix(S_box):
    for i in range(16):
        for j in range(16):
            S_box[i][j] = inverse(S_box[i][j])


# 字节变换
def byte_conversion(S_box):
    c = ''.join(reversed(list('01100011')))
    for i in range(16):
        for j in range(16):
            b = ''.join(reversed(h2b(S_box[i][j])))
            b_ = ''
            for k in range(8):
                b_ += str(int(b[k]) ^ int(b[(k + 4) % 8]) ^ int(b[(k + 5) % 8]) ^ int(b[(k + 6) % 8]) ^ int(
                    b[(k + 7) % 8]) ^ int(c[k]))
            S_box[i][j] = b2h(''.join(reversed(list(b_))))


# 逆字节变换
def byte_conversion_(S_box):
    c = ''.join(reversed(list('00000101')))
    for i in range(16):
        for j in range(16):
            b = ''.join(reversed(h2b(S_box[i][j])))
            b_ = ''
            for k in range(8):
                b_ += str(int(b[(k + 2) % 8]) ^ int(b[(k + 5) % 8]) ^ int(b[(k + 7) % 8]) ^ int(c[k]))
            S_box[i][j] = b2h(''.join(reversed(list(b_))))


def main():
    # 初始化的初始化
    S_box = [([0] * 16) for _ in range(16)]
    init(S_box)
    inverse_matrix(S_box)
    byte_conversion(S_box)
    print_matrix(S_box)
    print()
    init(S_box)
    byte_conversion_(S_box)
    inverse_matrix(S_box)
    print_matrix(S_box)


if __name__ == "__main__":
    main()
