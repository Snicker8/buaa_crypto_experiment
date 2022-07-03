def bbs(l, n, s):
    X = []
    B = 0
    X.append(s * s % n)
    for i in range(1, l + 1):
        X.append(X[i - 1] * X[i - 1] % n)
        B += (X[i] % 2) << (i - 1)
    return B


def main():
    l = int(input())  # 需要生成的随机比特位数
    p = int(input())
    q = int(input())
    s = int(input())
    n = p * q
    print(bbs(l, n, s))
    return 0


if __name__ == "__main__":
    main()
