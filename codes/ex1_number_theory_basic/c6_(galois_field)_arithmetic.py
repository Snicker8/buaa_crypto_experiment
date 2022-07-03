def addORminus(a1, a2):
    return hex(a1 ^ a2)[2:].zfill(2)


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
    return hex(res)[2:].zfill(2)


def divide(a1, a2):
    len1, len2 = a1.bit_length(), a2.bit_length()
    len = len1 - len2 + 1
    if len < 1: return '00 ' + hex(a1)[2:]
    div = 0
    while len1 >= len2:
        a1 ^= (a2 << (len1 - len2))
        div ^= (1 << (len1 - len2))
        len1 = a1.bit_length()
    return hex(div)[2:].zfill(2) + ' ' + hex(a1)[2:].zfill(2)


def main():
    a1, op, a2 = input().split()
    a1, a2 = int(a1, 16), int(a2, 16)

    if op == '+' or op == '-':
        print(addORminus(a1, a2))
    elif op == '*':
        print(multiply(a1, a2))
    else:
        print(divide(a1, a2))


if __name__ == '__main__':
    main()
