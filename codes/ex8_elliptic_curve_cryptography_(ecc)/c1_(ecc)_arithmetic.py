# 有限域上ECC的四则运算


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


# ECC加法
def add(x1, y1, x2, y2, a, p):
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


# ECC乘法_快速模幂
def times(x1, y1, a, p, k):
    # 计算n的二进制表示
    k_bin = bin(k)[2:]
    [x3, y3] = [0, 0]
    for k_i in k_bin:
        [x3, y3] = add(x3, y3, x3, y3, a, p)
        if k_i == '1':
            [x3, y3] = add(x3, y3, x1, y1, a, p)
    return [x3, y3]


if __name__ == '__main__':
    p = int(input())
    a = int(input())
    b = int(input())
    x1, y1 = [int(i) for i in input().split()]
    x2, y2 = [int(i) for i in input().split()]
    k = int(input())

    print(" ".join(str(i) for i in add(x1, y1, x2, y2, a, p)))
    print(" ".join(str(i) for i in add(x1, y1, x2, -y2, a, p)))
    print(" ".join(str(i) for i in times(x1, y1, a, p, k)))
    print(" ".join(str(i) for i in times(x2, y2, a, p, mr(k, p))))
