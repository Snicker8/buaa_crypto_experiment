def gcd(a, b):
    while a % b != 0:
        a, b = b, (a % b)
    return b


# 求逆元
def mod_inv(e1, e2):
    A11, A12, A13 = e1, 1, 0
    A21, A22, A23 = e2, 0, 1
    while A21 != 0:
        r = A11 // A21
        A11, A12, A13, A21, A22, A23 = A21, A22, A23, A11 - r * A21, A12 - r * A22, A13 - r * A23
    return A12 % e2


# 字母转数字
def l2n(s):
    for i in range(len(s)):
        s[i] = ord(s[i]) - 97
    return s


# 数字转字母
def n2l(n):
    for i in range(len(n)):
        n[i] = chr(n[i] + 97)
    return n


# 判断密钥是否合法
def illegal(k, b):
    if k == 0:
        return 1
    elif gcd(k, 26) != 1:
        return 1
    elif k == 1 and b == 1:
        return 1
    else:
        return 0


# 放射密码加密
def affine_enc(k, b, s):
    for i in range(len(s)):
        s[i] = (k * s[i] + b) % 26
    return s


# 放射密码解密
def affine_dec(k, b, s):
    for i in range(len(s)):
        s[i] = (mod_inv(k, 26) * (s[i] - b)) % 26
    return s


def main():
    k, b = [int(i) for i in input().split()]
    s = list(input().strip().replace('\n', '').replace('\r', ''))
    model_ = int(input())

    if illegal(k, b):
        print('invalid key')
    else:
        l2n(s)
        affine_enc(k, b, s) if model_ else affine_dec(k, b, s)
        n2l(s)
        for i in s:
            print(i, end='')


if __name__ == "__main__":
    main()
