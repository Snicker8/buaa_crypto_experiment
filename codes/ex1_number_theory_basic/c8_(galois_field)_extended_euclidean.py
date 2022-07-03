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


def ExEuclid(a, b):
    x1, y1, x2, y2 = 1, 0, 0, 1
    while b:
        q, r = divide(a, b)
        a, b = b, r
        x1, x2 = x2, x1 ^ multiply(q, x2)
        y1, y2 = y2, y1 ^ multiply(q, y2)
    return hex(x1)[2:].zfill(2) + ' ' + hex(y1)[2:].zfill(2) + ' ' + hex(a)[2:].zfill(2)


def main():
    a, b = input().split()
    a, b = int(a, 16), int(b, 16)
    print(ExEuclid(a, b))


if __name__ == '__main__':
    main()
