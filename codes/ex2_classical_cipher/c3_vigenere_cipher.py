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


# 弗吉尼亚加解密
def Vigenere_enc(k, p):
    for i in range(len(p)):
        p[i] = (p[i] + k[i % len(k)]) % 26
    return p


def Vigenere_dec(k, c):
    for i in range(len(c)):
        c[i] = (c[i] - k[i % len(k)]) % 26
    return c


def main():
    k = list(input().strip().replace('\n', '').replace('\r', ''))
    s = list(input().strip().replace('\n', '').replace('\r', ''))
    model_ = int(input())
    l2n(k)
    l2n(s)
    Vigenere_enc(k, s) if model_ else Vigenere_dec(k, s)
    n2l(s)
    for i in s: print(i, end='')


if __name__ == "__main__":
    main()
