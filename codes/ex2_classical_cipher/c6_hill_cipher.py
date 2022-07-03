# letter & number
def l2n(s):
    for i in range(len(s)):
        s[i] = ord(s[i]) - 97
    return s


def n2l(n):
    for i in range(len(n)):
        n[i] = chr(n[i] + 97)
    return n


# 行向量矩阵乘
def multiply(M, K):
    C = []
    for j in range(len(M)):
        sum = 0
        for i in range(len(M)):
            sum += M[i] * K[i][j]
        C.append(sum % 26)
    return C


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
        return s


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
def Hill(n, K, s):
    i = 0
    while i < len(s):
        s[i: i + n] = multiply(s[i: i + n], K)
        i += n
    return s


if __name__ == "__main__":
    n = int(input())
    K = []
    for i in range(n):
        K.append([int(i) for i in input().split()])
    s = list(input().strip().replace('\n', '').replace('\r', ''))
    model_ = int(input())
    l2n(s)
    Hill(n, K, s) if model_ else Hill(n, inv(K), s)
    n2l(s)
    print(''.join(s))
