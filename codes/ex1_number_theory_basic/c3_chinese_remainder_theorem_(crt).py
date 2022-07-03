# 求模逆（返回扩欧中的x）
def mr(e, m):
    A11, A12, A13 = e, 1, 0
    A21, A22, A23 = m, 0, 1
    while A21 != 0:
        r = A11 // A21
        A11, A12, A13, A21, A22, A23 = A21, A22, A23, A11 - r * A21, A12 - r * A22, A13 - r * A23
    return A12 % m


# 中国剩余定理
def CRT(a1, m1, a2, m2, a3, m3):
    """
        方程组
        x = a1 (mod m1)
        x = a2 (mod m2)
        x = a3 (mod m3)
    """
    M1, M2, M3 = m2 * m3, m1 * m3, m1 * m2
    M1_, M2_, M3_ = mr(M1, m1), mr(M2, m2), mr(M3, m3)
    x = (M1 * M1_ * a1 + M2 * M2_ * a2 + M3 * M3_ * a3) % (m1 * m2 * m3)
    return x


def main():
    m1, m2, m3 = [int(i) for i in input().split()]
    a1, a2, a3 = [int(i) for i in input().split()]

    # 奇葩样例（为什么答案不是0？？？）
    if CRT(a1, m1, a2, m2, a3, m3) == 0:
        print(m1 * m2 * m3)
    else:
        print(CRT(a1, m1, a2, m2, a3, m3))


if __name__ == '__main__':
    main()
