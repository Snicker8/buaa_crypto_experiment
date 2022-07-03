# 字符转数字
def s2n(s):
    for i in range(len(s)):
        s[i] = ord(s[i])
    return s


# 数字转字符
def n2s(n):
    for i in range(len(n)):
        n[i] = chr(n[i])
    return n


# 弗纳姆加解密（完全一样）
def Vernam_enc(k, p):
    for i in range(len(p)):
        p[i] = p[i] ^ k[i % len(k)]
    return p


def Vernam_dec(k, c):
    for i in range(len(c)):
        c[i] = c[i] ^ k[i % len(k)]
    return c


def main():
    k = list(input().strip().replace('\n', '').replace('\r', ''))
    s = list(input().strip().replace('\n', '').replace('\r', ''))
    model_ = int(input())
    s2n(k)
    s2n(s)
    Vernam_enc(k, s) if model_ else Vernam_dec(k, s)
    n2s(s)
    for i in s: print(i, end='')


if __name__ == "__main__":
    main()
