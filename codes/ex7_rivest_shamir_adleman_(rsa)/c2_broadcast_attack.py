import gmpy2


# 中国剩余定理
def crt(b, m):
    # 判断是否互素
    for i in range(len(m)):
        for j in range(i + 1, len(m)):
            if gmpy2.gcd(m[i], m[j]) != 1:
                print("m中含有不是互余的数")
                return -1
    # 乘积
    M = 1
    for i in range(len(m)):
        M *= m[i]
    # 求M/mi
    Mm = []
    for i in range(len(m)):
        Mm.append(M // m[i])
    # 求Mm[i]的乘法逆元
    Mm_ = []
    for i in range(len(m)):
        Mm_.append(gmpy2.invert(Mm[i], m[i]) % m[i])
    # 求MiMi_bi的累加
    y = 0
    for i in range(len(m)):
        y += (Mm[i] * Mm_[i] * b[i])
        y %= M
    return y


def main():
    n = int(input())
    e = int(input())
    c = []
    N = []
    for _ in range(n):
        c.append(int(input()))
        N.append(int(input()))
    # 求出密文m_c
    m_c = crt(c, N)
    # 开根求出明文m
    m = gmpy2.iroot(m_c, e)[0]
    print(m)


if __name__ == "__main__":
    main()
