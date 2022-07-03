import random


# letter & number
def l2n(s):
    for i in range(len(s)):
        s[i] = ord(s[i]) - 97
    return s


# gcd
def gcd(a, b):
    while a % b != 0:
        a, b = b, (a % b)
    return b


# 同维矩阵乘
def multiply(n, a, b):
    c = [([0] * n) for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                c[i][j] += a[i][k] * b[k][j]
                c[i][j] %= 26
    return c


# 代数余子式algebraic cofactor
def cof(m, i, j):
    return [[row[col] for col in range(len(m)) if col != j] for row in m[:i] + m[i + 1:]]


# 求行列式（递归）
def det(m):
    if len(m) == 1:
        return m[0][0]
    else:  # 按列展开
        s = 0
        for j in range(len(m)):
            n = cof(m, 0, j)
            if j % 2 == 0:
                s += m[0][j] * det(n)
            else:
                s -= m[0][j] * det(n)
        return s % 26


# 数模26逆
def mr(n):
    a11, a12, a13 = n, 1, 0
    a21, a22, a23 = 26, 0, 1
    while a21 != 0:
        r = a11 // a21
        a11, a12, a13, a21, a22, a23 = a21, a22, a23, a11 - r * a21, a12 - r * a22, a13 - r * a23
    return a12 % 26


# 矩阵模26逆
def inv(m):
    inv_m = [([0] * len(m)) for _ in range(len(m))]
    for i in range(len(m)):
        for j in range(len(m)):
            if (i + j) % 2:
                inv_m[j][i] = (-1) * det(cof(m, i, j)) * mr(det(m)) % 26
            else:
                inv_m[j][i] = det(cof(m, i, j)) * mr(det(m)) % 26
    return inv_m


# Hill密码加解密（分组乘即可）
def pt_att(n, p, c):
    P = []
    C = []
    for i in range(len(p) // n):
        P.append(p[i * n: (i + 1) * n])
        C.append(c[i * n: (i + 1) * n])

    index = list(range(len(P)))
    P_n = [([0] * n) for _ in range(n)]
    while gcd(det(P_n), 26) != 1:
        choose = random.sample(index, n)
        P_n = []
        C_n = []
        for i in choose:
            P_n.append(P[i])
            C_n.append(C[i])

    return multiply(n, inv(P_n), C_n)


def main():
    n = int(input())
    m = list(input().strip().replace('\n', '').replace('\r', ''))
    c = list(input().strip().replace('\n', '').replace('\r', ''))

    l2n(m)
    l2n(c)
    K = pt_att(n, m, c)
    for i in range(n):
        for j in range(n):
            print(K[i][j], end=' ')
        print()


if __name__ == "__main__":
    main()
