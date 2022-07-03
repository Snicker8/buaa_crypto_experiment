def multiply(a1, a2):
    res = 0
    while a2:
        if a2 & 1:
            res = res ^ a1
        a1, a2 = a1 << 1, a2 >> 1
    return res


def divide(a1, a2):
    len1, len2 = a1.bit_length(), a2.bit_length()
    len = len1 - len2 + 1
    if len < 1: return '00 ' + hex(a1)[2:]
    div = 0
    while len1 >= len2:
        a1 ^= (a2 << (len1 - len2))
        div ^= (1 << (len1 - len2))
        len1 = a1.bit_length()
    return a1 == 0  # 整除返回True


def main():
    polys = list(range(1, 512))
    polys[0] = 0
    for i in range(2, 512):
        for j in range(i, 512):
            m = multiply(i, j) - 1
            if m <= 510:
                polys[m] = 0
    intpolys = [poly for poly in polys if poly != 0 and poly >= 256]

    m = 2 ** 8 - 1
    for i in range(len(intpolys)):
        if divide(2 ** m + 1, intpolys[i]) is False:
            intpolys[i] = 0
            continue
        for q in range(m):
            if divide(2 ** q + 1, intpolys[i]) is True:
                intpolys[i] = 0
                break
    prpolys = [intpoly for intpoly in intpolys if intpoly != 0]
    for prpoly in prpolys:
        print(bin(prpoly)[2:], end=' ')


if __name__ == '__main__':
    main()
