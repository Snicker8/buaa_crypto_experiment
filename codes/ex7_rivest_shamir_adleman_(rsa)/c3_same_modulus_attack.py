import gmpy2


# 快速模幂
def fastpow(x, k, m):
    if k < 0:
        return fastpow(gmpy2.invert(x, m), -k, m)
    a = 1
    while k:
        if k & 1:
            a = a * x % m
        k = k >> 1
        x = x * x % m
    return a


# 扩展欧几里得
def gcd_expand(a1, a2):
    if a2 == 0:
        return a1, 1, 0
    elif a1 == 0:
        return a2, 0, 1
    else:
        GCD, xtmp, ytmp = gcd_expand(a2, a1 % a2)
        x = ytmp
        y = xtmp - ytmp * (a1 // a2)
        return GCD, x, y


def main():
    e1 = int(input())
    e2 = int(input())
    c1 = int(input())
    c2 = int(input())
    N = int(input())
    _, s1, s2 = gcd_expand(e1, e2)
    m = fastpow(c1, s1, N) * fastpow(c2, s2, N)
    m %= N
    print(m)
    return 0


if __name__ == "__main__":
    main()
