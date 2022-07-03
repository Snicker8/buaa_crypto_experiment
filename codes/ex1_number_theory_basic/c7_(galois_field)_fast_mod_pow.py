def multiply(a1, a2):
    res = 0
    poly = int('100011011', 2)
    digit_1 = poly.bit_length() - 1
    while a2:
        if a2 & 1:
            res = res ^ a1
        a1, a2 = a1 << 1, a2 >> 1
        if a1 >> digit_1:  # 取出 a1 的最高位
            a1 = a1 ^ poly
    return res


# a ^ k mod p
def pow_mod(a, k):
    res = 1
    while k:
        if k & 1:  # 如果 n 是奇数
            res = multiply(res, a)
        k = k // 2
        a = multiply(a, a)
    return hex(res)[2:]


def main():
    a, k = input().split()
    a, k = int(a, 16), int(k)
    print(pow_mod(a, k))


if __name__ == '__main__':
    main()
